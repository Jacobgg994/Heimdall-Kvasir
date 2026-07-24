import { create } from 'zustand'
import type { DeviceInfo, DeviceProfile } from '../types'

interface DeviceState {
  devices: DeviceInfo[]
  selectedSerial: string | null
  selectedGroup: string | null
  view: 'grid' | 'device' | 'flows' | 'health' | 'content' | 'settings'

  // Actions
  setDevices: (devices: DeviceInfo[]) => void
  addDevice: (device: DeviceInfo) => void
  removeDevice: (serial: string) => void
  updateDevice: (serial: string, updates: Partial<DeviceInfo>) => void
  selectDevice: (serial: string | null) => void
  setView: (view: DeviceState['view']) => void
  setSelectedGroup: (groupId: string | null) => void

  // Computed
  getSelectedDevice: () => DeviceInfo | undefined
  getDevicesByGroup: (groupId: string) => DeviceInfo[]
}

export const useDeviceStore = create<DeviceState>((set, get) => ({
  devices: [],
  selectedSerial: null,
  selectedGroup: null,
  view: 'grid',

  setDevices: (devices) => set({ devices }),

  addDevice: (device) =>
    set((state) => {
      const existing = state.devices.findIndex((d) => d.serial === device.serial)
      if (existing >= 0) {
        const updated = [...state.devices]
        updated[existing] = device
        return { devices: updated }
      }
      return { devices: [...state.devices, device] }
    }),

  removeDevice: (serial) =>
    set((state) => ({
      devices: state.devices.filter((d) => d.serial !== serial),
      selectedSerial: state.selectedSerial === serial ? null : state.selectedSerial
    })),

  updateDevice: (serial, updates) =>
    set((state) => ({
      devices: state.devices.map((d) =>
        d.serial === serial ? { ...d, ...updates } : d
      )
    })),

  selectDevice: (serial) =>
    set({
      selectedSerial: serial,
      view: serial ? 'device' : 'grid'
    }),

  setView: (view) => set({ view }),

  setSelectedGroup: (groupId) => set({ selectedGroup: groupId }),

  getSelectedDevice: () => {
    const { devices, selectedSerial } = get()
    return devices.find((d) => d.serial === selectedSerial)
  },

  getDevicesByGroup: (groupId) => {
    return get().devices.filter((d) => d.tags?.includes(groupId))
  }
}))
