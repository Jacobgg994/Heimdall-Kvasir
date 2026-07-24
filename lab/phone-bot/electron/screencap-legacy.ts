import { AdbExecutor } from './adb-executor'
import { CONFIG } from './config'
import type { ScreenFrame } from '../src/types'

type FrameCallback = (frame: ScreenFrame) => void

interface CaptureSession {
  serial: string
  interval: ReturnType<typeof setInterval>
  callback: FrameCallback
  width: number
  height: number
}

export class ScreencapLegacy {
  private adb: AdbExecutor
  private sessions: Map<string, CaptureSession> = new Map()

  constructor() {
    this.adb = new AdbExecutor()
  }

  /**
   * Start periodic screencap for a device.
   * This is Phase 0 fallback — Phase 1 replaces with scrcpy H.264 streaming.
   */
  async startCapturing(serial: string, callback: FrameCallback): Promise<void> {
    // Stop existing session if any
    this.stopCapturing(serial)

    // Get device resolution
    const size = await this.adb.getScreenSize(serial)
    const width = size?.width || 1080
    const height = size?.height || 1920

    const session: CaptureSession = {
      serial,
      callback,
      width,
      height,
      interval: setInterval(async () => {
        try {
          const frame = await this.captureOnce(serial)
          callback(frame)
        } catch {
          // Frame capture failed — device might be busy
        }
      }, CONFIG.screencapInterval)
    }

    // Capture first frame immediately
    try {
      const firstFrame = await this.captureOnce(serial)
      callback(firstFrame)
    } catch {
      // Will retry on next interval
    }

    this.sessions.set(serial, session)
  }

  /**
   * Stop screencap loop for a device
   */
  stopCapturing(serial: string): void {
    const session = this.sessions.get(serial)
    if (session) {
      clearInterval(session.interval)
      this.sessions.delete(serial)
    }
  }

  /**
   * Stop all capture sessions
   */
  stopAll(): void {
    for (const [serial] of this.sessions) {
      this.stopCapturing(serial)
    }
  }

  /**
   * Capture a single screenshot from a device.
   * Uses exec-out for direct binary stream (faster than file-based pull).
   */
  async captureOnce(serial: string): Promise<ScreenFrame> {
    const now = Date.now()

    try {
      // exec-out screencap -p returns PNG directly
      const buffer = await this.adb.execOut(serial, 'screencap -p')

      // Convert to base64 JPEG for transport.
      // In production, use sharp for resize+convert.
      // For Phase 0 MVP, return as PNG base64.
      const base64 = buffer.toString('base64')

      return {
        serial,
        data: `data:image/png;base64,${base64}`,
        width: 0, // Will be set by image natural dimensions on renderer
        height: 0,
        timestamp: now,
        format: 'png'
      }
    } catch (error) {
      const errMsg = error instanceof Error ? error.message : String(error)
      throw new Error(`Screencap failed for ${serial}: ${errMsg}`)
    }
  }

  /**
   * Get number of active capture sessions
   */
  get activeSessionCount(): number {
    return this.sessions.size
  }
}
