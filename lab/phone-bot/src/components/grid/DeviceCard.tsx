import { useEffect, useState } from 'react'
import type { DeviceInfo, DeviceBattery, DeviceStorage } from '../../types'
import { phoneBot } from '../../api'
import { HealthOverlay } from '../health/HealthOverlay'

interface Props {
  device: DeviceInfo
  onClick: () => void
}

export function DeviceCard({ device, onClick }: Props) {
  const [thumbnail, setThumbnail] = useState<string | null>(null)
  const isOnline = device.state === 'online'

  useEffect(() => {
    if (!isOnline) return

    phoneBot.takeScreenshot(device.serial).then((frame) => {
      setThumbnail(frame.data)
    }).catch(() => {
      // Device might be busy
    })
  }, [device.serial, isOnline])

  return (
    <div
      className={`device-card ${!isOnline ? 'offline' : ''}`}
      onClick={onClick}
    >
      <div className="card-thumbnail">
        {thumbnail ? (
          <img src={thumbnail} alt={device.serial} />
        ) : (
          <span style={{ fontSize: 32, opacity: 0.2 }}>
            {isOnline ? '📱' : '📴'}
          </span>
        )}
        <div style={{ position: 'absolute', top: 4, right: 4, display: 'flex', gap: 3 }}>
          <span className={`status-dot ${device.state}`} />
        </div>
      </div>

      <div className="card-info">
        <div className="card-name" style={{ display: 'flex', justifyContent: 'space-between' }}>
          <span>{device.model || device.serial.split(':')[0]}</span>
          {device.battery && (
            <HealthOverlay
              battery={device.battery}
              storage={device.storage}
              compact
            />
          )}
        </div>
        <div className="card-meta">
          {device.resolution && `${device.resolution} · `}
          {device.transport === 'wifi' ? '📶 WiFi' : '🔌 USB'}
          {device.androidVersion && ` · Android ${device.androidVersion}`}
        </div>
        {device.tags && device.tags.length > 0 && (
          <div style={{ display: 'flex', gap: 3, marginTop: 2 }}>
            {device.tags.map((tag) => (
              <span
                key={tag}
                style={{
                  fontSize: 9,
                  padding: '1px 5px',
                  borderRadius: 3,
                  background: 'var(--bg-elevated)',
                  color: 'var(--text-secondary)'
                }}
              >
                {tag}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
