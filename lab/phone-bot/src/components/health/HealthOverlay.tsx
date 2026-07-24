import type { DeviceBattery, DeviceStorage } from '../../types'

interface Props {
  battery?: DeviceBattery | null
  storage?: DeviceStorage | null
  compact?: boolean
}

export function HealthOverlay({ battery, storage, compact = false }: Props) {
  if (!battery && !storage) return null

  const tempClass = battery
    ? battery.temperature > 42 ? 'crit' : battery.temperature > 38 ? 'warn' : 'good'
    : 'good'

  const batteryClass = battery
    ? battery.level <= 15 ? 'crit' : battery.level <= 30 ? 'warn' : 'good'
    : 'good'

  const storageClass = storage
    ? storage.percent >= 95 ? 'crit' : storage.percent >= 85 ? 'warn' : 'good'
    : 'good'

  if (compact) {
    return (
      <div style={{ display: 'flex', gap: 4, alignItems: 'center' }}>
        {battery && (
          <>
            <span className={`health-badge ${batteryClass}`}>
              🔋{battery.level}%
            </span>
            <span className={`health-badge ${tempClass}`}>
              {battery.temperature}°C
            </span>
          </>
        )}
        {storage && storage.percent > 80 && (
          <span className={`health-badge ${storageClass}`}>
            💾{storage.percent}%
          </span>
        )}
      </div>
    )
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 2, fontSize: 10, fontFamily: "'JetBrains Mono', monospace" }}>
      {battery && (
        <>
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span className={`status-dot ${batteryClass}`} style={{ width: 6, height: 6 }} />
            <span style={{ color: 'var(--text-secondary)' }}>Battery:</span>
            <span>{battery.level}%</span>
            {battery.charging && <span style={{ color: 'var(--accent)' }}>⚡</span>}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span className={`status-dot ${tempClass}`} style={{ width: 6, height: 6 }} />
            <span style={{ color: 'var(--text-secondary)' }}>Temp:</span>
            <span>{battery.temperature}°C</span>
            <span style={{ color: 'var(--text-muted)' }}>{battery.health}</span>
          </div>
        </>
      )}
      {storage && (
        <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
          <span className={`status-dot ${storageClass}`} style={{ width: 6, height: 6 }} />
          <span style={{ color: 'var(--text-secondary)' }}>Storage:</span>
          <span>{storage.percent}% used</span>
          <span style={{ color: 'var(--text-muted)' }}>
            ({formatBytes(storage.free)} free)
          </span>
        </div>
      )}
    </div>
  )
}

function formatBytes(bytes: number): string {
  if (bytes === 0) return '0B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + sizes[i]
}
