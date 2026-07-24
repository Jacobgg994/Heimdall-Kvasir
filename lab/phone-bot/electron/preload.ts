import { contextBridge, ipcRenderer } from 'electron'

// Define the API exposed to the renderer
const phoneBotAPI = {
  // ── Devices ────────────────────────────────────────────────
  getDevices: () => ipcRenderer.invoke('devices:list'),
  getDeviceProfile: (serial: string) => ipcRenderer.invoke('devices:profile', serial),
  updateDeviceProfile: (serial: string, profile: Record<string, unknown>) =>
    ipcRenderer.invoke('devices:profile:update', serial, profile),
  connectDevice: (address: string) => ipcRenderer.invoke('devices:connect', address),
  disconnectDevice: (serial: string) => ipcRenderer.invoke('devices:disconnect', serial),

  // ── Screen ─────────────────────────────────────────────────
  subscribeScreen: (serial: string) => ipcRenderer.invoke('screen:subscribe', serial),
  unsubscribeScreen: (serial: string) => ipcRenderer.invoke('screen:unsubscribe', serial),
  takeScreenshot: (serial: string) => ipcRenderer.invoke('screen:screenshot', serial),

  // ── Input ──────────────────────────────────────────────────
  sendCommand: (command: unknown) => ipcRenderer.invoke('input:command', command),
  broadcastCommand: (serials: string[], command: unknown) =>
    ipcRenderer.invoke('input:broadcast', serials, command),

  // ── Window Controls ────────────────────────────────────────
  minimizeWindow: () => ipcRenderer.invoke('window:minimize'),
  maximizeWindow: () => ipcRenderer.invoke('window:maximize'),
  closeWindow: () => ipcRenderer.invoke('window:close'),
  isMaximized: () => ipcRenderer.invoke('window:isMaximized'),

  // ── Event Listeners (Main → Renderer) ─────────────────────
  onDeviceAdded: (callback: (device: unknown) => void) => {
    const handler = (_event: Electron.IpcRendererEvent, device: unknown) => callback(device)
    ipcRenderer.on('device:added', handler)
    return () => ipcRenderer.removeListener('device:added', handler)
  },
  onDeviceRemoved: (callback: (serial: string) => void) => {
    const handler = (_event: Electron.IpcRendererEvent, serial: string) => callback(serial)
    ipcRenderer.on('device:removed', handler)
    return () => ipcRenderer.removeListener('device:removed', handler)
  },
  onDeviceStatus: (callback: (data: { serial: string; status: string }) => void) => {
    const handler = (_event: Electron.IpcRendererEvent, data: { serial: string; status: string }) =>
      callback(data)
    ipcRenderer.on('device:status', handler)
    return () => ipcRenderer.removeListener('device:status', handler)
  },
  onFrame: (callback: (frame: unknown) => void) => {
    const handler = (_event: Electron.IpcRendererEvent, frame: unknown) => callback(frame)
    ipcRenderer.on('device:frame', handler)
    return () => ipcRenderer.removeListener('device:frame', handler)
  },
  onStreamMode: (callback: (data: { serial: string; mode: string }) => void) => {
    const handler = (_event: Electron.IpcRendererEvent, data: { serial: string; mode: string }) =>
      callback(data)
    ipcRenderer.on('device:stream_mode', handler)
    return () => ipcRenderer.removeListener('device:stream_mode', handler)
  },
  getScrcpyStatus: (serial: string) => ipcRenderer.invoke('screen:scrcpy_status', serial),

  // ── Health ─────────────────────────────────────────────────
  startHealthMonitor: (serial: string) => ipcRenderer.invoke('health:start', serial),
  stopHealthMonitor: (serial: string) => ipcRenderer.invoke('health:stop', serial),
  getHealthSnapshot: (serial: string) => ipcRenderer.invoke('health:snapshot', serial),
  getAllHealthSnapshots: () => ipcRenderer.invoke('health:all'),
  onHealthBattery: (callback: (data: { serial: string; battery: Record<string, unknown> }) => void) => {
    const handler = (_event: Electron.IpcRendererEvent, data: { serial: string; battery: Record<string, unknown> }) =>
      callback(data)
    ipcRenderer.on('health:battery', handler)
    return () => ipcRenderer.removeListener('health:battery', handler)
  },
  onHealthStorage: (callback: (data: { serial: string; storage: Record<string, unknown> }) => void) => {
    const handler = (_event: Electron.IpcRendererEvent, data: { serial: string; storage: Record<string, unknown> }) =>
      callback(data)
    ipcRenderer.on('health:storage', handler)
    return () => ipcRenderer.removeListener('health:storage', handler)
  },
  onHealthAlert: (callback: (alert: unknown) => void) => {
    const handler = (_event: Electron.IpcRendererEvent, alert: unknown) => callback(alert)
    ipcRenderer.on('health:alert', handler)
    return () => ipcRenderer.removeListener('health:alert', handler)
  },
  onHealthSnapshot: (callback: (snapshot: unknown) => void) => {
    const handler = (_event: Electron.IpcRendererEvent, snapshot: unknown) => callback(snapshot)
    ipcRenderer.on('health:snapshot', handler)
    return () => ipcRenderer.removeListener('health:snapshot', handler)
  },

  // ── Groups ─────────────────────────────────────────────────
  getGroups: () => ipcRenderer.invoke('groups:list'),
  createGroup: (group: { name: string; color: string; deviceSerials: string[] }) =>
    ipcRenderer.invoke('groups:create', group),
  updateGroup: (group: { id: string; name?: string; color?: string }) =>
    ipcRenderer.invoke('groups:update', group),
  deleteGroup: (groupId: string) => ipcRenderer.invoke('groups:delete', groupId),
  assignToGroup: (serial: string, groupId: string) => ipcRenderer.invoke('groups:assign', serial, groupId)
}

// Expose the API to the renderer process
contextBridge.exposeInMainWorld('phoneBotAPI', phoneBotAPI)

// Type declaration for renderer
export type PhoneBotAPI = typeof phoneBotAPI
