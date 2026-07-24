import { useEffect, useState } from 'react';
import './App.css';
import ChatPanel from './components/ChatPanel';
import TeamPanel from './components/TeamPanel';
import FilePanel from './components/FilePanel';
import SettingsPanel from './components/SettingsPanel';
import AgentPanel from './components/AgentPanel';
import TeamSidebar from './components/TeamSidebar';
import useStore from './stores/useStore';

const tabs = [
  { id: 'chat', label: '💬 Chat' },
  { id: 'agents', label: '🤖 Agents' },
  { id: 'team', label: '👥 Team' },
  { id: 'files', label: '📂 Files' },
  { id: 'settings', label: '⚙️ Config' },
];

function App() {
  const { activeTab, setTab, theme, toggleTheme } = useStore();
  const [showTeamBar, setShowTeamBar] = useState(() => {
    const saved = localStorage.getItem('showTeamBar');
    return saved !== null ? saved === 'true' : true;
  });

  useEffect(() => {
    localStorage.setItem('showTeamBar', showTeamBar);
  }, [showTeamBar]);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  const renderPanel = () => {
    switch (activeTab) {
      case 'chat': return <ChatPanel />;
      case 'agents': return <AgentPanel />;
      case 'team': return <TeamPanel />;
      case 'files': return <FilePanel />;
      case 'settings': return <SettingsPanel />;
      default: return <ChatPanel />;
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      width: '100vw',
      overflow: 'hidden',
      background: 'var(--bg)',
    }}>
      {/* Top bar */}
      <div className="top-bar" style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: 40,
        padding: '0 16px',
        borderBottom: '1px solid var(--border)',
        background: 'var(--bg)',
        flexShrink: 0,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span className="top-bar-title" style={{ color: 'var(--accent)', fontWeight: 600, fontSize: 14 }}>JACOB CC</span>
          <span className="hide-mobile" style={{ color: 'var(--text-secondary)', fontSize: 11 }}>·</span>
          <span className="hide-mobile" style={{ color: 'var(--text-secondary)', fontSize: 11 }}>localhost</span>
          <span className="hide-mobile" style={{ color: 'var(--text-secondary)', fontSize: 11 }}>·</span>
          <span className="hide-mobile" style={{ color: '#3b82f6', fontSize: 11 }}>deepseek-v4-pro[1m]</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <div className="top-bar-tabs" style={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setTab(tab.id)}
                style={{
                  background: activeTab === tab.id ? 'var(--border)' : 'transparent',
                  color: activeTab === tab.id ? 'var(--accent)' : 'var(--text-secondary)',
                  border: 'none',
                  padding: '4px 10px',
                  fontSize: 12,
                  fontFamily: 'JetBrains Mono, monospace',
                  cursor: 'pointer',
                  borderRadius: 0,
                  transition: 'none',
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>
          {/* Team sidebar toggle */}
          <button
            onClick={() => setShowTeamBar((v) => !v)}
            style={{
              background: showTeamBar ? 'var(--border)' : 'transparent',
              border: 'none',
              cursor: 'pointer',
              fontSize: 13,
              padding: '4px 6px',
              marginLeft: 2,
              color: showTeamBar ? 'var(--accent)' : 'var(--text-secondary)',
              fontFamily: 'JetBrains Mono, monospace',
              lineHeight: 1,
            }}
            title="Toggle team sidebar"
          >
            👥
          </button>
          <button
            onClick={toggleTheme}
            style={{
              background: 'transparent',
              border: 'none',
              cursor: 'pointer',
              fontSize: 14,
              padding: '4px 6px',
              marginLeft: 2,
              color: 'var(--text-secondary)',
              fontFamily: 'JetBrains Mono, monospace',
            }}
          >
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>
        </div>
      </div>

      {/* Content */}
      <div style={{ flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'row' }}>
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
          {renderPanel()}
        </div>
        {showTeamBar && <TeamSidebar />}
      </div>
    </div>
  );
}

export default App;
