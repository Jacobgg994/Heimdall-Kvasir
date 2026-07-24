import { useDeviceStore } from '../../hooks/useDevices'
import { phoneBot } from '../../api'
import { AlertBadge } from '../health/AlertBadge'

export function TopBar() {
  const { view, setView, devices, selectedSerial, selectDevice } = useDeviceStore()
  const onlineCount = devices.filter((d) => d.state === 'online').length

  return (
    <div className="titlebar">
      <div className="titlebar-left">
        <span style={{ fontSize: 14, fontWeight: 700, color: 'var(--accent)', marginRight: 8 }}>
          📱 Phone Bot
        </span>
        <button
          className={`nav-tab ${view === 'grid' ? 'active' : ''}`}
          onClick={() => {
            selectDevice(null)
            setView('grid')
          }}
        >
          📋 Grid
        </button>
        <button
          className={`nav-tab ${view === 'flows' ? 'active' : ''}`}
          onClick={() => setView('flows')}
        >
          ⚡ Flows
        </button>
        <button
          className={`nav-tab ${view === 'health' ? 'active' : ''}`}
          onClick={() => setView('health')}
        >
          💚 Health
        </button>
        <button
          className={`nav-tab ${view === 'content' ? 'active' : ''}`}
          onClick={() => setView('content')}
        >
          📁 Content
        </button>
        <button
          className={`nav-tab ${view === 'settings' ? 'active' : ''}`}
          onClick={() => setView('settings')}
        >
          ⚙️ Settings
        </button>

        {selectedSerial && view === 'device' && (
          <span style={{ fontSize: 11, color: 'var(--text-secondary)', marginLeft: 8 }} className="mono">
            ← {selectedSerial}
          </span>
        )}
      </div>

      <div className="titlebar-center">
        <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
          <span className={`status-dot ${onlineCount > 0 ? 'online' : 'offline'}`} />
          {' '}{onlineCount}/{devices.length} online
        </span>
        <AlertBadge />
      </div>

      <div className="titlebar-right">
        <button className="titlebar-btn" onClick={() => phoneBot.minimizeWindow()} title="Minimize">
          ─
        </button>
        <button className="titlebar-btn" onClick={() => phoneBot.maximizeWindow()} title="Maximize">
          □
        </button>
        <button className="titlebar-btn close" onClick={() => phoneBot.closeWindow()} title="Close">
          ✕
        </button>
      </div>
    </div>
  )
}
