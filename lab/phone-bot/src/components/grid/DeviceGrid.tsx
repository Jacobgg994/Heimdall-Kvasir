import { useState } from 'react'
import { useDeviceStore } from '../../hooks/useDevices'
import { DeviceCard } from './DeviceCard'
import { phoneBot } from '../../api'

export function DeviceGrid() {
  const { devices, selectDevice, selectedGroup } = useDeviceStore()
  const [connectAddress, setConnectAddress] = useState('')

  const filtered = selectedGroup
    ? devices.filter((d) => d.tags?.includes(selectedGroup))
    : devices

  const handleConnect = async () => {
    if (!connectAddress.trim()) return
    await phoneBot.connectDevice(connectAddress.trim())
    setConnectAddress('')
  }

  if (devices.length === 0) {
    return (
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <div className="connect-bar">
          <input
            type="text"
            placeholder="Connect device: 192.168.x.x:5555"
            value={connectAddress}
            onChange={(e) => setConnectAddress(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleConnect()}
          />
          <button className="action-btn primary" onClick={handleConnect}>
            Connect
          </button>
        </div>
        <div className="empty-state">
          <div className="icon">📱</div>
          <div className="title">No Devices Connected</div>
          <div className="subtitle">
            Connect your Android phones via USB or WiFi ADB.
            For WiFi: enable USB debugging, then run{' '}
            <code className="mono" style={{ color: 'var(--accent)' }}>adb tcpip 5555</code>
            {' '}and enter the IP above.
          </div>
        </div>
      </div>
    )
  }

  return (
    <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
      <div className="connect-bar">
        <input
          type="text"
          placeholder="Connect: 192.168.x.x:5555"
          value={connectAddress}
          onChange={(e) => setConnectAddress(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleConnect()}
        />
        <button className="action-btn primary" onClick={handleConnect}>
          Connect
        </button>
        <span style={{ fontSize: 11, color: 'var(--text-muted)', marginLeft: 8 }}>
          {filtered.length} of {devices.length} devices
        </span>
        {selectedGroup && (
          <button
            className="action-btn"
            onClick={() => useDeviceStore.getState().setSelectedGroup(null)}
            style={{ marginLeft: 'auto' }}
          >
            ✕ Clear filter
          </button>
        )}
      </div>
      <div className="device-grid">
        {filtered.map((device) => (
          <DeviceCard
            key={device.serial}
            device={device}
            onClick={() => selectDevice(device.serial)}
          />
        ))}
      </div>
    </div>
  )
}
