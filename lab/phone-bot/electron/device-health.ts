import { EventEmitter } from 'events'
import { AdbExecutor } from './adb-executor'
import { CONFIG } from './config'
import type { DeviceBattery, DeviceStorage, DeviceHealthAlert } from '../src/types'

export interface HealthSnapshot {
  serial: string
  timestamp: number
  battery: DeviceBattery | null
  storage: DeviceStorage | null
  foregroundApp: string | null
  uptime: number | null       // seconds since boot
  isHealthy: boolean
  alerts: DeviceHealthAlert[]
}

export class DeviceHealth extends EventEmitter {
  private adb: AdbExecutor
  private monitors: Map<string, ReturnType<typeof setInterval>> = new Map()
  private snapshots: Map<string, HealthSnapshot> = new Map()
  private alertHistory: Map<string, DeviceHealthAlert[]> = new Map()

  // Thresholds
  private readonly TEMP_WARN = 38    // °C
  private readonly TEMP_CRIT = 42    // °C
  private readonly BATTERY_LOW = 15  // %
  private readonly STORAGE_WARN = 85 // %
  private readonly STORAGE_CRIT = 95 // %

  // Cooldown to avoid alert spam (ms)
  private readonly ALERT_COOLDOWN = 300000 // 5 minutes

  constructor() {
    super()
    this.adb = new AdbExecutor()
  }

  /**
   * Start monitoring a device
   */
  startMonitoring(serial: string): void {
    if (this.monitors.has(serial)) return

    // Initial check
    this.checkDevice(serial)

    // Periodic monitoring
    const interval = setInterval(() => {
      this.checkDevice(serial)
    }, CONFIG.healthCheckInterval)

    this.monitors.set(serial, interval)
    this.alertHistory.set(serial, [])
  }

  /**
   * Stop monitoring a device
   */
  stopMonitoring(serial: string): void {
    const interval = this.monitors.get(serial)
    if (interval) {
      clearInterval(interval)
      this.monitors.delete(serial)
    }
  }

  /**
   * Stop all monitoring
   */
  stopAll(): void {
    for (const [serial] of this.monitors) {
      this.stopMonitoring(serial)
    }
  }

  /**
   * Get latest health snapshot for a device
   */
  getSnapshot(serial: string): HealthSnapshot | undefined {
    return this.snapshots.get(serial)
  }

  /**
   * Get all snapshots
   */
  getAllSnapshots(): Map<string, HealthSnapshot> {
    return this.snapshots
  }

  /**
   * Get active monitors count
   */
  get activeMonitorCount(): number {
    return this.monitors.size
  }

  // ─── Health Check ──────────────────────────────────────────

  private async checkDevice(serial: string): Promise<void> {
    const alerts: DeviceHealthAlert[] = []
    let battery: DeviceBattery | null = null
    let storage: DeviceStorage | null = null
    let foregroundApp: string | null = null
    let uptime: number | null = null

    try {
      // Battery info
      battery = await this.readBattery(serial)
      if (battery) {
        if (battery.temperature >= this.TEMP_CRIT) {
          alerts.push(this.createAlert(serial, 'battery_temp', 'critical',
            `🔥 Critical temp: ${battery.temperature}°C! Risk of battery swelling.`))
        } else if (battery.temperature >= this.TEMP_WARN) {
          alerts.push(this.createAlert(serial, 'battery_temp', 'warning',
            `🌡️ High temp: ${battery.temperature}°C. Consider pausing automation.`))
        }

        if (battery.level <= this.BATTERY_LOW) {
          alerts.push(this.createAlert(serial, 'battery_low', 'warning',
            `🔋 Low battery: ${battery.level}%. Device may shut down.`))
        }

        // Emit battery event for live UI updates
        this.emit('battery:update', { serial, battery })
      }

      // Storage info
      storage = await this.readStorage(serial)
      if (storage) {
        if (storage.percent >= this.STORAGE_CRIT) {
          alerts.push(this.createAlert(serial, 'storage_full', 'critical',
            `💾 Storage critically full: ${storage.percent}%. Clean TikTok cache!`))
        } else if (storage.percent >= this.STORAGE_WARN) {
          alerts.push(this.createAlert(serial, 'storage_full', 'warning',
            `💾 Storage filling: ${storage.percent}%. ${this.formatBytes(storage.free)} free.`))
        }

        this.emit('storage:update', { serial, storage })
      }

      // Foreground app check
      foregroundApp = await this.readForegroundApp(serial)
      this.emit('foreground:update', { serial, foregroundApp })

      // Uptime
      uptime = await this.readUptime(serial)
    } catch {
      // Device might be offline
    }

    const snapshot: HealthSnapshot = {
      serial,
      timestamp: Date.now(),
      battery,
      storage,
      foregroundApp,
      uptime,
      isHealthy: alerts.filter(a => a.severity === 'critical').length === 0,
      alerts
    }

    this.snapshots.set(serial, snapshot)

    // Emit alerts (with cooldown)
    for (const alert of alerts) {
      this.emitAlert(alert)
    }

    // Emit full snapshot
    this.emit('health:snapshot', snapshot)
  }

  // ─── ADB Readers ───────────────────────────────────────────

  private async readBattery(serial: string): Promise<DeviceBattery | null> {
    try {
      const output = await this.adb.shell(serial, 'dumpsys battery')
      const get = (key: string): string => {
        const match = output.match(new RegExp(`${key}:\\s*(.+)`))
        return match ? match[1].trim() : ''
      }

      const tempRaw = parseInt(get('temperature')) || 0
      // temperature is in 0.1°C from dumpsys
      const temperature = tempRaw > 100 ? tempRaw / 10 : tempRaw

      return {
        level: parseInt(get('level')) || 0,
        temperature,
        charging: get('AC powered') === 'true' || get('USB powered') === 'true',
        health: get('health') || 'Unknown',
        voltage: parseInt(get('voltage')) || 0
      }
    } catch {
      return null
    }
  }

  private async readStorage(serial: string): Promise<DeviceStorage | null> {
    try {
      const output = await this.adb.shell(serial, 'df -k /sdcard/')
      const lines = output.split('\n')
      if (lines.length < 2) return null

      // Parse: Filesystem 1K-blocks Used Available Use% Mounted on
      const parts = lines[1].trim().split(/\s+/)
      if (parts.length < 5) return null

      const total = parseInt(parts[1]) * 1024
      const used = parseInt(parts[2]) * 1024
      const free = parseInt(parts[3]) * 1024
      const percent = parseInt(parts[4])

      return { total, used, free, percent }
    } catch {
      return null
    }
  }

  private async readForegroundApp(serial: string): Promise<string | null> {
    try {
      const output = await this.adb.shell(serial,
        'dumpsys activity activities | grep mResumedActivity | head -1')
      // Format: mResumedActivity: ActivityRecord{... u0 com.example.app/.MainActivity t123}
      const match = output.match(/u0\s+([\w.]+)\//)
      return match ? match[1] : null
    } catch {
      return null
    }
  }

  private async readUptime(serial: string): Promise<number | null> {
    try {
      const output = await this.adb.shell(serial, 'cat /proc/uptime')
      const match = output.match(/^([\d.]+)/)
      return match ? parseFloat(match[1]) : null
    } catch {
      return null
    }
  }

  // ─── Alert Management ──────────────────────────────────────

  private createAlert(
    serial: string,
    type: DeviceHealthAlert['type'],
    severity: DeviceHealthAlert['severity'],
    message: string
  ): DeviceHealthAlert {
    return { serial, type, severity, message, timestamp: Date.now() }
  }

  private emitAlert(alert: DeviceHealthAlert): void {
    const history = this.alertHistory.get(alert.serial) || []

    // Cooldown: don't repeat same type within cooldown period
    const sameType = history.filter(a => a.type === alert.type && a.severity === alert.severity)
    const lastSame = sameType.length > 0 ? sameType[sameType.length - 1] : undefined
    if (lastSame && (alert.timestamp - lastSame.timestamp) < this.ALERT_COOLDOWN) {
      return
    }

    history.push(alert)
    // Keep only last 50 alerts
    if (history.length > 50) history.shift()
    this.alertHistory.set(alert.serial, history)

    this.emit('alert', alert)
  }

  // ─── Utility ───────────────────────────────────────────────

  private formatBytes(bytes: number): string {
    if (bytes === 0) return '0 B'
    const k = 1024
    const sizes = ['B', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i]
  }
}
