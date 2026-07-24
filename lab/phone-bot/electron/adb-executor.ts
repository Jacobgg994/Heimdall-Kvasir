import { exec, execSync } from 'child_process'
import { promisify } from 'util'
import { CONFIG } from './config'

const execAsync = promisify(exec)

export interface AdbDevice {
  serial: string
  state: 'device' | 'offline' | 'unauthorized' | 'no device'
}

export class AdbExecutor {
  /**
   * Execute an ADB command for a specific device.
   * Uses -s flag to target the device.
   */
  async exec(serial: string, command: string): Promise<string> {
    const cmd = `${CONFIG.adbPath} -s ${serial} ${command}`
    try {
      const { stdout, stderr } = await execAsync(cmd, {
        timeout: CONFIG.defaultTimeout
      })
      if (stderr && !stderr.includes('Warning')) {
        throw new Error(stderr.trim())
      }
      return stdout.trim()
    } catch (error) {
      const errMsg = error instanceof Error ? error.message : String(error)
      throw new Error(`ADB [${serial}] ${command}: ${errMsg}`)
    }
  }

  /**
   * Execute ADB command without targeting a specific device
   */
  async execGlobal(command: string): Promise<string> {
    const cmd = `${CONFIG.adbPath} ${command}`
    try {
      const { stdout, stderr } = await execAsync(cmd, {
        timeout: CONFIG.defaultTimeout
      })
      if (stderr && !stderr.includes('Warning')) {
        throw new Error(stderr.trim())
      }
      return stdout.trim()
    } catch (error) {
      const errMsg = error instanceof Error ? error.message : String(error)
      throw new Error(`ADB: ${errMsg}`)
    }
  }

  /**
   * Execute a shell command on a device via persistent shell session style.
   * For now uses individual exec calls; Phase 1 adds persistent shell pooling.
   */
  async shell(serial: string, command: string): Promise<string> {
    return this.exec(serial, `shell ${command}`)
  }

  /**
   * Execute shell command and return raw buffer (for screencap)
   */
  async shellBuffer(serial: string, command: string): Promise<Buffer> {
    const cmd = `${CONFIG.adbPath} -s ${serial} shell ${command}`
    try {
      const { stdout } = await execAsync(cmd, {
        timeout: CONFIG.defaultTimeout,
        encoding: 'buffer'
      })
      return stdout
    } catch (error) {
      const errMsg = error instanceof Error ? error.message : String(error)
      throw new Error(`ADB buffer [${serial}]: ${errMsg}`)
    }
  }

  /**
   * exec-out: stream binary output directly (for screencap PNG)
   */
  async execOut(serial: string, command: string): Promise<Buffer> {
    const cmd = `${CONFIG.adbPath} -s ${serial} exec-out ${command}`
    try {
      const { stdout } = await execAsync(cmd, {
        timeout: CONFIG.defaultTimeout,
        encoding: 'buffer',
        maxBuffer: 50 * 1024 * 1024 // 50MB for raw screencap
      })
      return stdout
    } catch (error) {
      const errMsg = error instanceof Error ? error.message : String(error)
      throw new Error(`ADB exec-out [${serial}]: ${errMsg}`)
    }
  }

  /**
   * List all connected ADB devices
   */
  async listDevices(): Promise<AdbDevice[]> {
    try {
      const output = await this.execGlobal('devices -l')
      const lines = output.split('\n').slice(1) // Skip header
      const devices: AdbDevice[] = []

      for (const line of lines) {
        const trimmed = line.trim()
        if (!trimmed) continue

        const parts = trimmed.split(/\s+/)
        if (parts.length >= 2) {
          devices.push({
            serial: parts[0],
            state: parts[1] as AdbDevice['state']
          })
        }
      }

      return devices
    } catch {
      return []
    }
  }

  /**
   * Connect to a device over TCP/IP
   */
  async connect(address: string): Promise<boolean> {
    try {
      const output = await this.execGlobal(`connect ${address}`)
      return output.includes('connected') || output.includes('already connected')
    } catch {
      return false
    }
  }

  /**
   * Disconnect a TCP/IP device
   */
  async disconnect(serial: string): Promise<void> {
    await this.execGlobal(`disconnect ${serial}`)
  }

  /**
   * Get device properties
   */
  async getProperties(serial: string): Promise<Record<string, string>> {
    try {
      const output = await this.shell(serial, 'getprop')
      const props: Record<string, string> = {}
      for (const line of output.split('\n')) {
        const match = line.match(/\[([^\]]+)\]:\s*\[([^\]]*)\]/)
        if (match) {
          props[match[1]] = match[2]
        }
      }
      return props
    } catch {
      return {}
    }
  }

  /**
   * Get device screen resolution
   */
  async getScreenSize(serial: string): Promise<{ width: number; height: number } | null> {
    try {
      const output = await this.shell(serial, 'wm size')
      const match = output.match(/(\d+)x(\d+)/)
      if (match) {
        return {
          width: parseInt(match[1], 10),
          height: parseInt(match[2], 10)
        }
      }
      return null
    } catch {
      return null
    }
  }

  /**
   * Check if ADB server is running
   */
  async isServerRunning(): Promise<boolean> {
    try {
      await this.execGlobal('devices')
      return true
    } catch {
      return false
    }
  }

  /**
   * Start ADB server
   */
  async startServer(): Promise<void> {
    await this.execGlobal('start-server')
  }

  /**
   * Kill ADB server
   */
  async killServer(): Promise<void> {
    try {
      execSync(`${CONFIG.adbPath} kill-server`, { timeout: 5000 })
    } catch {
      // Server might already be dead
    }
  }
}
