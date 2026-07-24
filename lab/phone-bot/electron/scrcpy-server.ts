import { AdbExecutor } from './adb-executor'
import { CONFIG } from './config'
import { spawn, ChildProcess } from 'child_process'
import { createReadStream, existsSync, readFileSync } from 'fs'
import { join } from 'path'
import { app } from 'electron'

export interface ScrcpySession {
  serial: string
  videoPort: number
  controlPort: number
  audioPort: number | null
  process: ChildProcess | null
  streams: {
    video: ChildProcess | null   // ffmpeg decoder
    control: ChildProcess | null  // control socket writer
  }
  status: 'starting' | 'running' | 'error' | 'stopped'
  error?: string
  startedAt: number
}

export type FrameCallback = (data: {
  serial: string
  data: string    // base64 JPEG frame
  width: number
  height: number
  timestamp: number
}) => void

export class ScrcpyServer {
  private adb: AdbExecutor
  private sessions: Map<string, ScrcpySession> = new Map()
  private frameCallbacks: Map<string, FrameCallback> = new Map()

  constructor() {
    this.adb = new AdbExecutor()
  }

  /**
   * Get the path to scrcpy-server.jar
   */
  private getJarPath(): string {
    // Check bundled JAR first
    const bundledJar = join(app.getAppPath(), 'server', 'scrcpy-server.jar')
    if (existsSync(bundledJar)) {
      return bundledJar
    }

    // Check system scrcpy installation
    const systemPaths = [
      '/usr/share/scrcpy/scrcpy-server.jar',
      '/usr/local/share/scrcpy/scrcpy-server.jar',
      '/opt/scrcpy/scrcpy-server.jar'
    ]
    for (const p of systemPaths) {
      if (existsSync(p)) return p
    }

    throw new Error(
      'scrcpy-server.jar not found. Install scrcpy: sudo apt install scrcpy\n' +
      'Or place scrcpy-server.jar in phone-bot/server/'
    )
  }

  /**
   * Start scrcpy server on a device.
   * Pushes JAR, launches server via app_process, sets up port forwarding.
   */
  async start(serial: string, onFrame: FrameCallback): Promise<ScrcpySession> {
    // Stop existing session
    await this.stop(serial)

    const jarPath = this.getJarPath()
    const deviceJarPath = '/data/local/tmp/scrcpy-server.jar'
    const session: ScrcpySession = {
      serial,
      videoPort: 0,
      controlPort: 0,
      audioPort: null,
      process: null,
      streams: { video: null, control: null },
      status: 'starting',
      startedAt: Date.now()
    }

    try {
      // 1. Push JAR to device
      await this.adb.exec(serial, `push "${jarPath}" ${deviceJarPath}`)

      // 2. Launch server via app_process with tunnel_forward
      // The server outputs port numbers (2 bytes each, big-endian) to stdout
      const shellCmd = `CLASSPATH=${deviceJarPath} app_process / com.genymobile.scrcpy.Server 3.0 tunnel_forward=true send_frame_meta=false`

      const proc = spawn(CONFIG.adbPath, ['-s', serial, 'shell', shellCmd], {
        stdio: ['ignore', 'pipe', 'pipe']
      })

      session.process = proc

      // 3. Read port numbers from server stdout
      const ports = await new Promise<{ video: number; control: number }>((resolve, reject) => {
        const timeout = setTimeout(() => {
          reject(new Error('Timeout waiting for scrcpy server ports'))
        }, 15000)

        let buffer = Buffer.alloc(0)

        proc.stdout!.on('data', (chunk: Buffer) => {
          buffer = Buffer.concat([buffer, chunk])

          // We need at least 4 bytes (2 ports × 2 bytes each)
          if (buffer.length >= 4) {
            clearTimeout(timeout)
            const videoPort = buffer.readUInt16BE(0)
            const controlPort = buffer.readUInt16BE(2)
            resolve({ video: videoPort, control: controlPort })
          }
        })

        proc.on('error', (err) => {
          clearTimeout(timeout)
          reject(err)
        })

        proc.on('exit', (code) => {
          clearTimeout(timeout)
          if (code !== null && code !== 0) {
            reject(new Error(`Server exited with code ${code}`))
          }
        })
      })

      session.videoPort = ports.video
      session.controlPort = ports.control

      // 4. Forward ports via ADB
      await this.adb.execGlobal(`forward tcp:${ports.video} tcp:${ports.video}`)
      await this.adb.execGlobal(`forward tcp:${ports.control} tcp:${ports.control}`)

      // 5. Start H.264 decoder (ffmpeg → JPEG frames)
      const decoder = this.startDecoder(serial, ports.video, onFrame)
      session.streams.video = decoder
      session.status = 'running'

      this.sessions.set(serial, session)
      this.frameCallbacks.set(serial, onFrame)

      return session
    } catch (error) {
      session.status = 'error'
      session.error = error instanceof Error ? error.message : String(error)
      this.sessions.set(serial, session)
      throw error
    }
  }

  /**
   * Start ffmpeg to decode H.264 stream → individual JPEG frames
   */
  private startDecoder(serial: string, port: number, onFrame: FrameCallback): ChildProcess {
    // ffmpeg: read raw H.264 from TCP socket, output one JPEG per frame
    const ffmpeg = spawn('ffmpeg', [
      '-f', 'h264',           // Input format: raw H.264
      '-i', `tcp://127.0.0.1:${port}`,  // Read from forwarded port
      '-f', 'image2pipe',     // Output format: image pipe
      '-vcodec', 'mjpeg',     // JPEG encoding
      '-q:v', '5',            // Quality (2-31, lower = better)
      '-r', '30',             // Frame rate
      '-vf', 'scale=iw:ih',   // Keep original size
      '-an',                  // No audio
      '-'
    ], {
      stdio: ['ignore', 'pipe', 'pipe']
    })

    // Buffer for reading JPEG frames
    // JPEG frames are separated by ffmpeg; each frame is a complete JPEG
    let buffer = Buffer.alloc(0)
    let width = 0
    let height = 0

    ffmpeg.stdout!.on('data', (chunk: Buffer) => {
      buffer = Buffer.concat([buffer, chunk])

      // Try to extract complete JPEG frames
      // Each complete JPEG starts with 0xFF 0xD8 and ends with 0xFF 0xD9
      while (true) {
        const startIdx = buffer.indexOf(Buffer.from([0xFF, 0xD8]))
        if (startIdx === -1) break

        const endIdx = buffer.indexOf(Buffer.from([0xFF, 0xD9]), startIdx + 2)
        if (endIdx === -1) break

        const frame = buffer.subarray(startIdx, endIdx + 2)
        buffer = buffer.subarray(endIdx + 2)

        // Extract dimensions from JPEG header (SOF0 marker)
        if (width === 0 && frame.length > 100) {
          for (let i = 0; i < frame.length - 8; i++) {
            if (frame[i] === 0xFF && frame[i + 1] === 0xC0) {
              height = frame.readUInt16BE(i + 5)
              width = frame.readUInt16BE(i + 7)
              break
            }
          }
        }

        const base64 = frame.toString('base64')

        onFrame({
          serial,
          data: `data:image/jpeg;base64,${base64}`,
          width,
          height,
          timestamp: Date.now()
        })
      }
    })

    ffmpeg.stderr!.on('data', (_data: Buffer) => {
      // ffmpeg logs to stderr; suppress for now
      // Could parse for resolution info: "Stream #0:0: Video: ... , 1080x1920"
    })

    ffmpeg.on('error', (err) => {
      console.error(`[Scrcpy] ffmpeg error for ${serial}:`, err.message)
    })

    ffmpeg.on('exit', (code) => {
      if (code !== 0 && code !== null) {
        console.error(`[Scrcpy] ffmpeg exited with code ${code} for ${serial}`)
      }
    })

    return ffmpeg
  }

  /**
   * Send a control command to the device via scrcpy control socket.
   * This is the fast path: ~5ms latency vs 700ms for adb shell input.
   */
  async sendControl(serial: string, buffer: Buffer): Promise<void> {
    const session = this.sessions.get(serial)
    if (!session || session.status !== 'running') {
      throw new Error(`No active scrcpy session for ${serial}`)
    }

    // Connect to control socket and send command
    const net = require('net')
    return new Promise((resolve, reject) => {
      const client = net.createConnection({ host: '127.0.0.1', port: session.controlPort }, () => {
        client.write(buffer)
        client.end()
        resolve()
      })

      client.on('error', reject)
      client.setTimeout(3000, () => {
        client.destroy()
        reject(new Error('Control socket timeout'))
      })
    })
  }

  /**
   * Stop scrcpy server on a device
   */
  async stop(serial: string): Promise<void> {
    const session = this.sessions.get(serial)
    if (!session) return

    // Kill ffmpeg decoder
    if (session.streams.video) {
      session.streams.video.kill('SIGKILL')
      session.streams.video = null
    }

    // Kill control stream
    if (session.streams.control) {
      session.streams.control.kill('SIGKILL')
      session.streams.control = null
    }

    // Kill server process on device
    if (session.process) {
      session.process.kill('SIGKILL')
      session.process = null
    }

    // Remove ADB forwards
    try {
      await this.adb.execGlobal(`forward --remove tcp:${session.videoPort}`)
      await this.adb.execGlobal(`forward --remove tcp:${session.controlPort}`)
    } catch {
      // Ports might already be removed
    }

    // Clean up device JAR
    try {
      await this.adb.shell(serial, 'rm -f /data/local/tmp/scrcpy-server.jar')
    } catch {
      // Device might be disconnected
    }

    session.status = 'stopped'
    this.sessions.delete(serial)
    this.frameCallbacks.delete(serial)
  }

  /**
   * Stop all scrcpy sessions
   */
  async stopAll(): Promise<void> {
    const serials = Array.from(this.sessions.keys())
    await Promise.all(serials.map(s => this.stop(s).catch(() => {})))
  }

  /**
   * Get session info
   */
  getSession(serial: string): ScrcpySession | undefined {
    return this.sessions.get(serial)
  }

  /**
   * Check if a scrcpy session is active
   */
  isActive(serial: string): boolean {
    const session = this.sessions.get(serial)
    return session?.status === 'running'
  }

  /**
   * Number of active sessions
   */
  get activeSessionCount(): number {
    let count = 0
    for (const s of this.sessions.values()) {
      if (s.status === 'running') count++
    }
    return count
  }
}
