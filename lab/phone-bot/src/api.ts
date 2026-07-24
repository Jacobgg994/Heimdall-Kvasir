// API wrapper — provides typed access to the Electron IPC bridge
// Using explicit function wrappers instead of direct window.phoneBotAPI
// to avoid TypeScript global augmentation complexity

import type { DeviceInfo, DeviceProfile, InputCommand, ScreenFrame, IPCFrameEvent } from './types'

const api = (): PhoneBotAPI => (window as any).phoneBotAPI

export const phoneBot = {
  // Devices
  getDevices: (): Promise<DeviceInfo[]> => api().getDevices(),
  getDeviceProfile: (serial: string): Promise<DeviceProfile | undefined> => api().getDeviceProfile(serial),
  updateDeviceProfile: (serial: string, profile: Record<string, unknown>): Promise<{ success: boolean }> =>
    api().updateDeviceProfile(serial, profile),
  connectDevice: (address: string): Promise<DeviceInfo | null> => api().connectDevice(address),
  disconnectDevice: (serial: string): Promise<{ success: boolean }> => api().disconnectDevice(serial),

  // Screen
  subscribeScreen: (serial: string): Promise<{ success: boolean }> => api().subscribeScreen(serial),
  unsubscribeScreen: (serial: string): Promise<{ success: boolean }> => api().unsubscribeScreen(serial),
  takeScreenshot: (serial: string): Promise<ScreenFrame> => api().takeScreenshot(serial),

  // Input
  sendCommand: (command: InputCommand): Promise<{ success: boolean; error?: string }> => api().sendCommand(command),
  broadcastCommand: (serials: string[], command: InputCommand): Promise<{ serial: string; success: boolean; error?: string }[]> =>
    api().broadcastCommand(serials, command),

  // Window
  minimizeWindow: (): Promise<void> => api().minimizeWindow(),
  maximizeWindow: (): Promise<void> => api().maximizeWindow(),
  closeWindow: (): Promise<void> => api().closeWindow(),
  isMaximized: (): Promise<boolean> => api().isMaximized(),

  // Events
  onDeviceAdded: (callback: (device: DeviceInfo) => void): (() => void) => api().onDeviceAdded(callback),
  onDeviceRemoved: (callback: (serial: string) => void): (() => void) => api().onDeviceRemoved(callback),
  onDeviceStatus: (callback: (data: { serial: string; status: string }) => void): (() => void) => api().onDeviceStatus(callback),
  onFrame: (callback: (frame: IPCFrameEvent) => void): (() => void) => api().onFrame(callback),
  onStreamMode: (callback: (data: { serial: string; mode: string }) => void): (() => void) => api().onStreamMode(callback),
  getScrcpyStatus: (serial: string): Promise<unknown> => api().getScrcpyStatus(serial),

  // Health
  startHealthMonitor: (serial: string): Promise<{ success: boolean }> => api().startHealthMonitor(serial),
  stopHealthMonitor: (serial: string): Promise<{ success: boolean }> => api().stopHealthMonitor(serial),
  getHealthSnapshot: (serial: string): Promise<unknown> => api().getHealthSnapshot(serial),
  getAllHealthSnapshots: (): Promise<Record<string, unknown>> => api().getAllHealthSnapshots(),
  onHealthBattery: (callback: (data: { serial: string; battery: Record<string, unknown> }) => void): (() => void) =>
    api().onHealthBattery(callback),
  onHealthStorage: (callback: (data: { serial: string; storage: Record<string, unknown> }) => void): (() => void) =>
    api().onHealthStorage(callback),
  onHealthAlert: (callback: (alert: unknown) => void): (() => void) => api().onHealthAlert(callback),
  onHealthSnapshot: (callback: (snapshot: unknown) => void): (() => void) => api().onHealthSnapshot(callback),

  // Groups
  getGroups: (): Promise<unknown[]> => api().getGroups(),
  createGroup: (group: { name: string; color: string; deviceSerials: string[] }): Promise<unknown> => api().createGroup(group),
  updateGroup: (group: { id: string; name?: string; color?: string }): Promise<{ success: boolean }> => api().updateGroup(group),
  deleteGroup: (groupId: string): Promise<{ success: boolean }> => api().deleteGroup(groupId),
  assignToGroup: (serial: string, groupId: string): Promise<{ success: boolean }> => api().assignToGroup(serial, groupId),
}

// Re-export the raw window API type for use elsewhere
interface PhoneBotAPI {
  getDevices: () => Promise<DeviceInfo[]>
  getDeviceProfile: (serial: string) => Promise<DeviceProfile | undefined>
  updateDeviceProfile: (serial: string, profile: Record<string, unknown>) => Promise<{ success: boolean }>
  connectDevice: (address: string) => Promise<DeviceInfo | null>
  disconnectDevice: (serial: string) => Promise<{ success: boolean }>
  subscribeScreen: (serial: string) => Promise<{ success: boolean; mode?: string }>
  unsubscribeScreen: (serial: string) => Promise<{ success: boolean }>
  takeScreenshot: (serial: string) => Promise<ScreenFrame>
  sendCommand: (command: InputCommand) => Promise<{ success: boolean; error?: string }>
  broadcastCommand: (serials: string[], command: InputCommand) => Promise<{ serial: string; success: boolean; error?: string }[]>
  minimizeWindow: () => Promise<void>
  maximizeWindow: () => Promise<void>
  closeWindow: () => Promise<void>
  isMaximized: () => Promise<boolean>
  onDeviceAdded: (callback: (device: DeviceInfo) => void) => () => void
  onDeviceRemoved: (callback: (serial: string) => void) => () => void
  onDeviceStatus: (callback: (data: { serial: string; status: string }) => void) => () => void
  onFrame: (callback: (frame: IPCFrameEvent) => void) => () => void
  onStreamMode: (callback: (data: { serial: string; mode: string }) => void) => () => void
  getScrcpyStatus: (serial: string) => Promise<unknown>
  startHealthMonitor: (serial: string) => Promise<{ success: boolean }>
  stopHealthMonitor: (serial: string) => Promise<{ success: boolean }>
  getHealthSnapshot: (serial: string) => Promise<unknown>
  getAllHealthSnapshots: () => Promise<Record<string, unknown>>
  onHealthBattery: (callback: (data: { serial: string; battery: Record<string, unknown> }) => void) => () => void
  onHealthStorage: (callback: (data: { serial: string; storage: Record<string, unknown> }) => void) => () => void
  onHealthAlert: (callback: (alert: unknown) => void) => () => void
  onHealthSnapshot: (callback: (snapshot: unknown) => void) => () => void
  getGroups: () => Promise<unknown[]>
  createGroup: (group: { name: string; color: string; deviceSerials: string[] }) => Promise<unknown>
  updateGroup: (group: { id: string; name?: string; color?: string }) => Promise<{ success: boolean }>
  deleteGroup: (groupId: string) => Promise<{ success: boolean }>
  assignToGroup: (serial: string, groupId: string) => Promise<{ success: boolean }>
}
