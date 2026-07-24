import { useEffect, useState } from 'react'
import { useDeviceStore } from '../../hooks/useDevices'
import { phoneBot } from '../../api'
import { HealthOverlay } from './HealthOverlay'

interface HealthSnap {
  serial: string
  timestamp: number
  battery: Record<string, unknown> | null
  storage: Record<string, unknown> | null
  foregroundApp: string | null
  uptime: number | null
  isHealthy: boolean
}

export function HealthPanel() {
  const { devices } = useDeviceStore()
  const [snapshots, setSnapshots] = useState<Record<string, HealthSnap>>({})

  useEffect(() => {
    phoneBot.getAllHealthSnapshots().then((data: Record<string, unknown>) => {
      setSnapshots(data as Record<string, HealthSnap>)
    })

    const unsub = phoneBot.onHealthSnapshot((snap: unknown) => {
      const s = snap as HealthSnap
      setSnapshots(prev => ({ ...prev, [s.serial]: s }))
    })

    return unsub
  }, [])

  const sorted = Object.values(snapshots).sort((a, b) => b.timestamp - a.timestamp)

  return (
    <div style={{ flex: 1, overflow: 'auto', padding: 16 }}>
      <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 12 }}>
        💚 Device Health Dashboard
      </div>

      {sorted.length === 0 && (
        <div className="empty-state">
          <div className="icon">💚</div>
          <div className="title">No Health Data</div>
          <div className="subtitle">Health monitoring starts automatically when devices connect.</div>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: 8 }}>
        {sorted.map(snap => {
          const device = devices.find(d => d.serial === snap.serial)
          return (
            <div
              key={snap.serial}
              style={{
                background: 'var(--bg-surface)',
                border: `1px solid ${snap.isHealthy ? 'var(--border-color)' : 'var(--accent-danger)'}`,
                borderRadius: 'var(--radius)',
                padding: 12
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                <span className="mono" style={{ fontSize: 12, fontWeight: 600 }}>
                  {device?.model || snap.serial.split(':')[0]}
                </span>
                <span className={`status-dot ${snap.isHealthy ? 'online' : 'offline'}`} />
              </div>

              <HealthOverlay
                battery={snap.battery as never}
                storage={snap.storage as never}
              />

              {snap.foregroundApp && (
                <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 6 }} className="mono">
                  App: {snap.foregroundApp}
                </div>
              )}

              {snap.uptime && (
                <div style={{ fontSize: 10, color: 'var(--text-muted)' }} className="mono">
                  Uptime: {formatUptime(snap.uptime)}
                </div>
              )}

              <div style={{ fontSize: 9, color: 'var(--text-muted)', marginTop: 4 }}>
                Updated: {new Date(snap.timestamp).toLocaleTimeString()}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

function formatUptime(seconds: number): string {
  const d = Math.floor(seconds / 86400)
  const h = Math.floor((seconds % 86400) / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  if (d > 0) return `${d}d ${h}h`
  if (h > 0) return `${h}h ${m}m`
  return `${m}m`
}
