import { phoneBot } from '../../api'
import type { InputCommand } from '../../types'

interface Props {
  serial: string
}

export function QuickActions({ serial }: Props) {
  const send = (action: InputCommand['action'], params?: Partial<InputCommand>) => {
    phoneBot.sendCommand({ serial, action, ...params } as InputCommand)
  }

  return (
    <div className="device-view-toolbar">
      <button className="action-btn" onClick={() => send('home')} title="Home (F1)">
        🏠 Home
      </button>
      <button className="action-btn" onClick={() => send('back')} title="Back (F2)">
        ⬅ Back
      </button>
      <button className="action-btn" onClick={() => send('recents')} title="Recents (F3)">
        ▢ Recents
      </button>

      <div style={{ width: 1, height: 20, background: 'var(--border-color)', margin: '0 4px' }} />

      <button className="action-btn" onClick={() => send('keyevent', { code: 26 })} title="Power">
        ⏻ Power
      </button>
      <button className="action-btn" onClick={() => send('keyevent', { code: 24 })} title="Volume Up">
        🔊 Vol+
      </button>
      <button className="action-btn" onClick={() => send('keyevent', { code: 25 })} title="Volume Down">
        🔉 Vol-
      </button>

      <div style={{ width: 1, height: 20, background: 'var(--border-color)', margin: '0 4px' }} />

      <button
        className="action-btn primary"
        onClick={() => phoneBot.takeScreenshot(serial)}
        title="Screenshot"
      >
        📷 Screenshot
      </button>

      <div style={{ width: 1, height: 20, background: 'var(--border-color)', margin: '0 4px' }} />

      <span style={{ fontSize: 10, color: 'var(--text-muted)' }} className="mono">
        {serial}
      </span>
    </div>
  )
}
