import { useState, useEffect } from 'react'
import type { DeviceHealthAlert } from '../../types'
import { phoneBot } from '../../api'

export function AlertBadge() {
  const [alerts, setAlerts] = useState<DeviceHealthAlert[]>([])
  const [expanded, setExpanded] = useState(false)

  useEffect(() => {
    const unsub = phoneBot.onHealthAlert((alert: unknown) => {
      const a = alert as DeviceHealthAlert
      setAlerts(prev => {
        const filtered = prev.filter(p => !(p.serial === a.serial && p.type === a.type))
        return [...filtered, a].slice(-20)
      })
    })
    return unsub
  }, [])

  const critical = alerts.filter(a => a.severity === 'critical')
  const warnings = alerts.filter(a => a.severity === 'warning')

  if (alerts.length === 0) return null

  return (
    <div style={{ position: 'relative' }}>
      <button
        className="nav-tab"
        onClick={() => setExpanded(!expanded)}
        style={{ position: 'relative' }}
      >
        {critical.length > 0 ? '🔴' : warnings.length > 0 ? '🟡' : '💚'}
        {' '}{alerts.length}
      </button>

      {expanded && (
        <div style={{
          position: 'absolute',
          top: '100%',
          right: 0,
          width: 320,
          maxHeight: 400,
          overflow: 'auto',
          background: 'var(--bg-elevated)',
          border: '1px solid var(--border-color)',
          borderRadius: 'var(--radius)',
          padding: 8,
          zIndex: 200,
          boxShadow: '0 4px 12px rgba(0,0,0,0.5)'
        }}>
          <div style={{ fontSize: 12, fontWeight: 600, marginBottom: 8, color: 'var(--text-secondary)' }}>
            Health Alerts
          </div>
          {alerts.slice().reverse().map((alert, i) => (
            <div
              key={`${alert.serial}-${alert.timestamp}-${i}`}
              style={{
                padding: '6px 8px',
                marginBottom: 4,
                borderRadius: 3,
                fontSize: 11,
                background: alert.severity === 'critical' ? '#3b0505' : '#3b2f05',
                borderLeft: `3px solid ${alert.severity === 'critical' ? 'var(--accent-danger)' : 'var(--accent-warning)'}`,
                fontFamily: "'JetBrains Mono', monospace"
              }}
            >
              <div style={{ color: 'var(--text-muted)', fontSize: 9, marginBottom: 2 }}>
                {alert.serial} · {new Date(alert.timestamp).toLocaleTimeString()}
              </div>
              <div>{alert.message}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
