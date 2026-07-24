import { AdbExecutor } from './adb-executor'
import { ScrcpyServer } from './scrcpy-server'
import {
  encodeTap, encodeSwipe, encodeKeyEvent, encodeTextEvent,
  encodeBackOrScreenOn, encodePowerMode,
  encodeExpandNotificationPanel, encodeCollapsePanels,
  KEYCODE, KEYCODE_ACTION, POWER_MODE
} from './scrcpy-input'
import type { InputCommand } from '../src/types'

export class InputController {
  private adb: AdbExecutor
  private scrcpy: ScrcpyServer | null = null

  constructor(scrcpy?: ScrcpyServer) {
    this.adb = new AdbExecutor()
    this.scrcpy = scrcpy || null
  }

  /**
   * Set scrcpy server reference for fast-path input
   */
  setScrcpyServer(scrcpy: ScrcpyServer): void {
    this.scrcpy = scrcpy
  }

  /**
   * Execute a single input command on a device.
   *
   * Auto-selects scrcpy control socket (5ms) when available,
   * falls back to adb shell input (700ms) otherwise.
   */
  async execute(command: InputCommand): Promise<{ success: boolean; error?: string }> {
    try {
      // Try scrcpy fast path first
      if (this.scrcpy?.isActive(command.serial)) {
        return await this.executeScrcpy(command)
      }

      // Fallback to ADB
      return await this.executeAdb(command)
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : String(error)
      }
    }
  }

  /**
   * Broadcast the same command to multiple devices in parallel
   */
  async broadcast(
    serials: string[],
    command: InputCommand
  ): Promise<{ serial: string; success: boolean; error?: string }[]> {
    const results = await Promise.all(
      serials.map(async (serial) => {
        const result = await this.execute({ ...command, serial })
        return { serial, ...result }
      })
    )
    return results
  }

  // ─── Scrcpy Fast Path (5ms) ────────────────────────────────

  private async executeScrcpy(cmd: InputCommand): Promise<{ success: boolean; error?: string }> {
    if (!this.scrcpy) {
      return { success: false, error: 'Scrcpy server not available' }
    }

    const session = this.scrcpy.getSession(cmd.serial)
    if (!session) {
      return { success: false, error: 'No active scrcpy session' }
    }

    const screenWidth = 1080  // Default, should get from device info
    const screenHeight = 1920

    let buffer: Buffer

    switch (cmd.action) {
      case 'tap': {
        const x = cmd.x || 0
        const y = cmd.y || 0
        const jx = cmd.xRandom ? Math.round((Math.random() * 2 - 1) * cmd.xRandom) : 0
        const jy = cmd.yRandom ? Math.round((Math.random() * 2 - 1) * cmd.yRandom) : 0
        buffer = encodeTap(x + jx, y + jy, screenWidth, screenHeight)
        break
      }

      case 'swipe': {
        const x1 = cmd.x1 || 0
        const y1 = cmd.y1 || 0
        const x2 = cmd.x2 || 0
        const y2 = cmd.y2 || 0
        const duration = cmd.duration || 300
        buffer = encodeSwipe(x1, y1, x2, y2, screenWidth, screenHeight, duration)
        break
      }

      case 'keyevent': {
        const code = cmd.code || 0
        buffer = encodeKeyEvent(code, KEYCODE_ACTION.DOWN)
        await this.scrcpy.sendControl(cmd.serial, buffer)
        buffer = encodeKeyEvent(code, KEYCODE_ACTION.UP)
        break
      }

      case 'text': {
        const text = cmd.value || ''
        buffer = encodeTextEvent(text)
        break
      }

      case 'home':
        buffer = encodeKeyEvent(KEYCODE.HOME, KEYCODE_ACTION.DOWN)
        await this.scrcpy.sendControl(cmd.serial, buffer)
        buffer = encodeKeyEvent(KEYCODE.HOME, KEYCODE_ACTION.UP)
        break

      case 'back':
        buffer = encodeBackOrScreenOn(0) // 0=BACK
        break

      case 'recents':
        buffer = encodeKeyEvent(KEYCODE.RECENTS, KEYCODE_ACTION.DOWN)
        await this.scrcpy.sendControl(cmd.serial, buffer)
        buffer = encodeKeyEvent(KEYCODE.RECENTS, KEYCODE_ACTION.UP)
        break

      default:
        // Fall through to ADB for unsupported actions
        return this.executeAdb(cmd)
    }

    await this.scrcpy.sendControl(cmd.serial, buffer)
    return { success: true }
  }

  // ─── ADB Fallback (700ms) ──────────────────────────────────

  private async executeAdb(cmd: InputCommand): Promise<{ success: boolean; error?: string }> {
    const { serial, action } = cmd

    switch (action) {
      case 'tap': {
        let x = cmd.x || 0
        let y = cmd.y || 0
        if (cmd.xRandom) x += Math.round((Math.random() * 2 - 1) * cmd.xRandom)
        if (cmd.yRandom) y += Math.round((Math.random() * 2 - 1) * cmd.yRandom)
        await this.adb.shell(serial, `input tap ${x} ${y}`)
        break
      }
      case 'swipe': {
        const x1 = cmd.x1 || 0, y1 = cmd.y1 || 0
        const x2 = cmd.x2 || 0, y2 = cmd.y2 || 0
        const duration = cmd.duration || 300
        await this.adb.shell(serial, `input swipe ${x1} ${y1} ${x2} ${y2} ${duration}`)
        break
      }
      case 'text': {
        const text = (cmd.value || '').replace(/'/g, "\\'").replace(/ /g, '%s')
        await this.adb.shell(serial, `input text '${text}'`)
        break
      }
      case 'keyevent':
        await this.adb.shell(serial, `input keyevent ${cmd.code || 0}`)
        break
      case 'home':
        await this.adb.shell(serial, 'input keyevent 3')
        break
      case 'back':
        await this.adb.shell(serial, 'input keyevent 4')
        break
      case 'recents':
        await this.adb.shell(serial, 'input keyevent 187')
        break
      case 'shell':
        if (cmd.command) await this.adb.shell(serial, cmd.command)
        break
      default:
        return { success: false, error: `Unknown action: ${action}` }
    }

    return { success: true }
  }
}
