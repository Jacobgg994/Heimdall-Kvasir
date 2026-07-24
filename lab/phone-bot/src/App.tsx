import { useEffect } from 'react'
import { TopBar } from './components/layout/TopBar'
import { DeviceGrid } from './components/grid/DeviceGrid'
import { GroupPanel } from './components/grid/GroupPanel'
import { DeviceView } from './components/device/DeviceView'
import { HealthPanel } from './components/health/HealthPanel'
import { useDeviceStore } from './hooks/useDevices'
import { phoneBot } from './api'
import type { DeviceInfo, DeviceBattery, DeviceStorage, DeviceHealthAlert } from './types'

export default function App() {
  const { view, setDevices, addDevice, removeDevice, updateDevice } = useDeviceStore()

  useEffect(() => {
    // Initial device list
    phoneBot.getDevices().then((devices: DeviceInfo[]) => {
      setDevices(devices)
    })

    // Device events
    const unsubAdded = phoneBot.onDeviceAdded((device: DeviceInfo) => {
      addDevice(device)
      phoneBot.startHealthMonitor(device.serial)
    })

    const unsubRemoved = phoneBot.onDeviceRemoved((serial: string) => {
      removeDevice(serial)
    })

    const unsubStatus = phoneBot.onDeviceStatus(({ serial, status }: { serial: string; status: string }) => {
      updateDevice(serial, {
        state: status as 'online' | 'offline' | 'busy' | 'unauthorized'
      })
    })

    // Health: battery updates
    const unsubBattery = phoneBot.onHealthBattery(({ serial, battery }: { serial: string; battery: Record<string, unknown> }) => {
      updateDevice(serial, {
        battery: battery as unknown as DeviceBattery
      })
    })

    // Health: storage updates
    const unsubStorage = phoneBot.onHealthStorage(({ serial, storage }: { serial: string; storage: Record<string, unknown> }) => {
      updateDevice(serial, {
        storage: storage as unknown as DeviceStorage
      })
    })

    // Poll
    const poll = setInterval(() => {
      phoneBot.getDevices().then((devices: DeviceInfo[]) => setDevices(devices))
    }, 5000)

    return () => {
      unsubAdded()
      unsubRemoved()
      unsubStatus()
      unsubBattery()
      unsubStorage()
      clearInterval(poll)
    }
  }, [])

  return (
    <div className="app-layout">
      <TopBar />
      <div className="app-content">
        {view !== 'device' && <GroupPanel />}
        <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
          {view === 'grid' && <DeviceGrid />}
          {view === 'device' && <DeviceView />}
          {view === 'health' && <HealthPanel />}
        </div>
      </div>
    </div>
  )
}
