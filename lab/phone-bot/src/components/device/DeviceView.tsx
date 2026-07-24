import { useEffect, useState } from 'react'
import { useDeviceStore } from '../../hooks/useDevices'
import { ScreenCanvas } from './ScreenCanvas'
import { QuickActions } from './QuickActions'
import { phoneBot } from '../../api'

export function DeviceView() {
  const { selectedSerial, devices, selectDevice } = useDeviceStore()
  const device = devices.find((d) => d.serial === selectedSerial)
  const [streamMode, setStreamMode] = useState<string>('unknown')

  useEffect(() => {
    if (!selectedSerial) return

    phoneBot.subscribeScreen(selectedSerial)

    const unsubStream = phoneBot.onStreamMode(({ serial, mode }) => {
      if (serial === selectedSerial) {
        setStreamMode(mode)
      }
    })

    return () => {
      phoneBot.unsubscribeScreen(selectedSerial)
      unsubStream()
    }
  }, [selectedSerial])

  if (!device) {
    return (
      <div className="empty-state">
        <div className="icon">📱</div>
        <div className="title">No Device Selected</div>
        <div className="subtitle">Select a device from the grid to view and control it.</div>
        <button className="action-btn" onClick={() => selectDevice(null)}>
          ← Back to Grid
        </button>
      </div>
    )
  }

  return (
    <div className="device-view">
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, width: '100%', padding: '0 12px' }}>
        <button className="action-btn" onClick={() => selectDevice(null)}>
          ← Back
        </button>
        <span className="mono" style={{ fontSize: 13, fontWeight: 600 }}>
          {device.model || device.serial}
        </span>
        <span className={`status-dot ${device.state}`} />
        <span style={{ fontSize: 11, color: 'var(--text-secondary)' }}>
          {device.resolution} · {device.transport === 'wifi' ? 'WiFi' : 'USB'}
        </span>
        {device.battery && (
          <span className={`health-badge ${device.battery.temperature > 42 ? 'crit' : device.battery.temperature > 38 ? 'warn' : 'good'}`}>
            🔋 {device.battery.level}% · {device.battery.temperature}°C
          </span>
        )}
        <span className={`health-badge ${streamMode === 'scrcpy' ? 'good' : streamMode === 'screencap' ? 'warn' : ''}`}>
          {streamMode === 'scrcpy' ? '⚡ 30FPS' : streamMode === 'screencap' ? '📷 6FPS' : '⏳ ...'}
        </span>
      </div>

      <ScreenCanvas serial={device.serial} />

      <QuickActions serial={device.serial} />
    </div>
  )
}
