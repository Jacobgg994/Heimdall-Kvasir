import { EventEmitter } from 'events'
import { AdbExecutor, AdbDevice } from './adb-executor'
import { CONFIG } from './config'
import type { DeviceInfo, DeviceProfile, DeviceGroup, ProxyConfig } from '../src/types'
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs'
import { join } from 'path'

interface PersistedData {
  groups: unknown[]
  accounts: unknown[]
  proxies: unknown[]
  flowHistory: unknown[]
  deviceProfiles: Record<string, DeviceProfile>
  version: number
}

export class DeviceManager extends EventEmitter {
  private adb: AdbExecutor
  private devices: Map<string, DeviceInfo> = new Map()
  private profiles: Map<string, DeviceProfile> = new Map()
  private groups: DeviceGroup[] = []
  private pollInterval: ReturnType<typeof setInterval> | null = null
  private knownDevices: Set<string> = new Set()

  constructor() {
    super()
    this.adb = new AdbExecutor()
    this.loadPersistedData()
    this.startPolling()
  }

  /**
   * Get all currently tracked devices
   */
  async listDevices(): Promise<DeviceInfo[]> {
    const rawDevices = await this.adb.listDevices()
    const now = Date.now()

    // Update state for all tracked devices
    for (const raw of rawDevices) {
      const existing = this.devices.get(raw.serial)

      if (raw.state === 'device') {
        if (!existing) {
          // New device
          const info = await this.buildDeviceInfo(raw)
          this.devices.set(raw.serial, info)
          this.knownDevices.add(raw.serial)
          this.emit('device:added', info)
        } else {
          existing.state = 'online'
          existing.lastSeen = now
        }
      } else if (raw.state === 'offline' || raw.state === 'unauthorized') {
        if (existing) {
          existing.state = raw.state
          existing.lastSeen = now
        }
        this.emit('device:status', raw.serial, raw.state)
      }
    }

    // Mark devices not in ADB list as offline
    const activeSerials = new Set(rawDevices.map(d => d.serial))
    for (const [serial, device] of this.devices) {
      if (!activeSerials.has(serial) && device.state === 'online') {
        device.state = 'offline'
        this.emit('device:status', serial, 'offline')
      }
    }

    return Array.from(this.devices.values())
  }

  /**
   * Connect to a device via TCP/IP
   */
  async connectDevice(address: string): Promise<DeviceInfo | null> {
    const success = await this.adb.connect(address)
    if (!success) return null

    // Give it a moment to register
    await this.delay(1000)

    // Find the newly connected device
    const devices = await this.adb.listDevices()
    const found = devices.find(d => d.serial === address || d.serial.includes(address.split(':')[0]))
    if (found && found.state === 'device') {
      const info = await this.buildDeviceInfo(found)
      this.devices.set(found.serial, info)
      this.knownDevices.add(found.serial)
      this.emit('device:added', info)
      return info
    }

    return null
  }

  /**
   * Disconnect a TCP/IP device
   */
  async disconnectDevice(serial: string): Promise<void> {
    const device = this.devices.get(serial)
    if (device?.transport === 'wifi') {
      await this.adb.disconnect(serial)
    }
    this.devices.delete(serial)
    this.knownDevices.delete(serial)
    this.emit('device:removed', serial)
  }

  /**
   * Get device profile with persisted data merged
   */
  getDeviceProfile(serial: string): DeviceProfile | undefined {
    return this.profiles.get(serial)
  }

  /**
   * Update device profile and persist
   */
  updateDeviceProfile(serial: string, updates: Partial<DeviceProfile>): void {
    const existing = this.profiles.get(serial) || {
      serial,
      tags: [],
      notes: ''
    }
    this.profiles.set(serial, { ...existing, ...updates })
    this.savePersistedData()
  }

  /**
   * Get all device groups
   */
  getAllGroups(): DeviceGroup[] {
    return this.groups.slice()
  }

  /**
   * Create a new device group
   */
  createGroup(group: Omit<DeviceGroup, 'id' | 'createdAt'>): DeviceGroup {
    const newGroup: DeviceGroup = {
      ...group,
      id: `grp_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`,
      createdAt: Date.now()
    }
    this.groups.push(newGroup)
    this.savePersistedData()
    return newGroup
  }

  /**
   * Update a device group
   */
  updateGroup(updates: Partial<DeviceGroup> & { id: string }): void {
    const idx = this.groups.findIndex(g => g.id === updates.id)
    if (idx >= 0) {
      this.groups[idx] = { ...this.groups[idx], ...updates }
      this.savePersistedData()
    }
  }

  /**
   * Delete a device group
   */
  deleteGroup(groupId: string): void {
    this.groups = this.groups.filter(g => g.id !== groupId)
    // Remove group from device tags
    for (const [serial, profile] of this.profiles) {
      if (profile.tags?.includes(groupId)) {
        profile.tags = profile.tags.filter(t => t !== groupId)
        this.profiles.set(serial, profile)
      }
    }
    this.savePersistedData()
  }

  /**
   * Assign a device to a group (adds group ID as tag)
   */
  assignToGroup(serial: string, groupId: string): void {
    const profile = this.profiles.get(serial) || { serial, tags: [], notes: '' }
    if (!profile.tags) profile.tags = []
    if (!profile.tags.includes(groupId)) {
      profile.tags.push(groupId)
      this.profiles.set(serial, profile)
      // Update live device info
      const device = this.devices.get(serial)
      if (device) {
        device.tags = [...profile.tags]
      }
      this.savePersistedData()
    }
  }

  /**
   * Clean up resources
   */
  cleanup(): void {
    if (this.pollInterval) {
      clearInterval(this.pollInterval)
      this.pollInterval = null
    }
  }

  // ─── Private Methods ───────────────────────────────────────

  private async buildDeviceInfo(raw: AdbDevice): Promise<DeviceInfo> {
    const now = Date.now()
    const isWifi = raw.serial.includes(':')
    const profile = this.profiles.get(raw.serial)

    // Get device details (non-blocking, don't fail if unavailable)
    const [props, screenSize] = await Promise.all([
      this.adb.getProperties(raw.serial).catch(() => ({}) as Record<string, string>),
      this.adb.getScreenSize(raw.serial).catch(() => null)
    ])

    const model = props['ro.product.model'] || 'Unknown'
    const androidVersion = props['ro.build.version.release'] || 'Unknown'

    const info: DeviceInfo = {
      serial: raw.serial,
      model,
      state: 'online',
      transport: isWifi ? 'wifi' : 'usb',
      ip: isWifi ? raw.serial.split(':')[0] : undefined,
      port: isWifi ? parseInt(raw.serial.split(':')[1] || '5555') : undefined,
      androidVersion,
      screenWidth: screenSize?.width,
      screenHeight: screenSize?.height,
      resolution: screenSize ? `${screenSize.width}x${screenSize.height}` : undefined,
      tags: profile?.tags || [],
      notes: profile?.notes || '',
      lastSeen: now,
      connectedAt: now
    }

    return info
  }

  private startPolling(): void {
    // Poll for device changes every 3 seconds using track-devices approach
    this.pollInterval = setInterval(async () => {
      try {
        await this.listDevices()
      } catch {
        // Silently handle polling errors
      }
    }, 3000)
  }

  private loadPersistedData(): void {
    const dataPath = join(CONFIG.dataDir, 'phone-bot-data.json')
    try {
      if (existsSync(dataPath)) {
        const raw = readFileSync(dataPath, 'utf-8')
        const data: PersistedData = JSON.parse(raw)
        if (data.deviceProfiles) {
          for (const [serial, profile] of Object.entries(data.deviceProfiles)) {
            this.profiles.set(serial, profile)
          }
        }
        if (data.groups) {
          this.groups = data.groups as DeviceGroup[]
        }
      }
    } catch {
      // Start fresh
    }
  }

  private savePersistedData(): void {
    const dataPath = join(CONFIG.dataDir, 'phone-bot-data.json')
    try {
      if (!existsSync(CONFIG.dataDir)) {
        mkdirSync(CONFIG.dataDir, { recursive: true })
      }
      const profiles: Record<string, DeviceProfile> = {}
      for (const [serial, profile] of this.profiles) {
        profiles[serial] = profile
      }
      const data: PersistedData = {
        groups: this.groups,
        accounts: [],
        proxies: [],
        flowHistory: [],
        deviceProfiles: profiles,
        version: 1
      }
      writeFileSync(dataPath, JSON.stringify(data, null, 2), 'utf-8')
    } catch {
      // Silently fail persistence
    }
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms))
  }
}
