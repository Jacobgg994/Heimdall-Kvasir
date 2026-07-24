import { useState } from 'react';
import useStore from '../stores/useStore';

export default function SettingsPanel() {
  const { isAuthenticated, login, logout, token } = useStore();
  const [password, setPassword] = useState('');
  const [loginError, setLoginError] = useState('');
  const [loggingIn, setLoggingIn] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!password) return;
    setLoggingIn(true);
    setLoginError('');
    try {
      const success = await login(password);
      if (success) {
        setPassword('');
      } else {
        setLoginError('invalid password');
      }
    } catch {
      setLoginError('connection error');
    } finally {
      setLoggingIn(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      background: 'var(--bg)',
      fontFamily: 'JetBrains Mono, monospace',
      fontSize: 13,
    }}>
      {/* Header */}
      <div style={{
        padding: '8px 16px',
        borderBottom: '1px solid var(--border)',
        display: 'flex',
        alignItems: 'center',
        gap: 8,
      }}>
        <span style={{ color: 'var(--accent)' }}>$</span>
        <span style={{ color: 'var(--text)' }}>cat /etc/config</span>
      </div>

      {/* Content */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: 16,
      }}>
        {/* Auth section */}
        <div style={{ marginBottom: 24 }}>
          <div style={{ color: 'var(--accent)', marginBottom: 8 }}>
            {`# ${isAuthenticated ? 'auth status: connected' : 'auth status: disconnected'}`}
          </div>
          <div style={{ color: 'var(--text-secondary)', marginBottom: 12 }}>
            {isAuthenticated
              ? '# you are authenticated. token stored in localStorage.'
              : '# enter your API password to connect to the backend.'}
          </div>

          {isAuthenticated ? (
            <div style={{ marginLeft: 16 }}>
              <div style={{ color: 'var(--accent)', marginBottom: 4 }}>
                {'✓ connected'}
              </div>
              <div style={{ color: 'var(--text-secondary)', fontSize: 12, marginBottom: 8 }}>
                token: {token?.substring(0, 24)}...
              </div>
              <button
                onClick={logout}
                style={{
                  background: 'transparent',
                  color: '#ef4444',
                  border: '1px solid #ef4444',
                  padding: '2px 10px',
                  fontSize: 12,
                  fontFamily: 'JetBrains Mono, monospace',
                  cursor: 'pointer',
                }}
              >
                $ logout
              </button>
            </div>
          ) : (
            <form onSubmit={handleLogin} style={{ marginLeft: 16 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                <span style={{ color: 'var(--text-secondary)' }}>$</span>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="enter password..."
                  style={{
                    background: 'transparent',
                    border: '1px solid #333',
                    color: 'var(--text)',
                    fontFamily: 'JetBrains Mono, monospace',
                    fontSize: 13,
                    padding: '4px 8px',
                    outline: 'none',
                    width: 240,
                  }}
                />
              </div>
              {loginError && (
                <div style={{ color: '#ef4444', marginLeft: 16, marginBottom: 8 }}>
                  {`✗ ${loginError}`}
                </div>
              )}
              <button
                type="submit"
                disabled={!password || loggingIn}
                style={{
                  background: 'transparent',
                  color: password && !loggingIn ? 'var(--accent)' : '#555',
                  border: password && !loggingIn ? '1px solid #22c55e' : '1px solid #333',
                  padding: '2px 10px',
                  fontSize: 12,
                  fontFamily: 'JetBrains Mono, monospace',
                  cursor: password && !loggingIn ? 'pointer' : 'not-allowed',
                }}
              >
                {loggingIn ? 'connecting...' : '$ connect'}
              </button>
            </form>
          )}
        </div>

        {/* API Status */}
        <div style={{ marginBottom: 24 }}>
          <div style={{ color: 'var(--accent)', marginBottom: 8 }}>
            {'# /etc/hosts'}
          </div>
          <div style={{ marginLeft: 16 }}>
            <div style={{ marginBottom: 4 }}>
              <span style={{ color: 'var(--text-secondary)' }}>api.backend  </span>
              <span style={{ color: 'var(--text)' }}>http://localhost:8000</span>
            </div>
            <div style={{ marginBottom: 4 }}>
              <span style={{ color: 'var(--text-secondary)' }}>api.status   </span>
              <span style={{ color: 'var(--accent)' }}>✓ ready</span>
            </div>
            <div style={{ marginBottom: 4 }}>
              <span style={{ color: 'var(--text-secondary)' }}>auth.status  </span>
              <span style={{ color: isAuthenticated ? 'var(--accent)' : '#eab308' }}>
                {isAuthenticated ? '✓ authenticated' : '⚠ not authenticated'}
              </span>
            </div>
          </div>
        </div>

        {/* Theme */}
        <div>
          <div style={{ color: 'var(--accent)', marginBottom: 8 }}>
            {'# ~/.config/theme'}
          </div>
          <div style={{ marginLeft: 16 }}>
            <div style={{ marginBottom: 4 }}>
              <span style={{ color: 'var(--text-secondary)' }}>name    </span>
              <span style={{ color: 'var(--text)' }}>terminal-dark</span>
            </div>
            <div style={{ marginBottom: 4 }}>
              <span style={{ color: 'var(--text-secondary)' }}>bg      </span>
              <span style={{ color: 'var(--text)' }}>#0a0a0a</span>
            </div>
            <div style={{ marginBottom: 4 }}>
              <span style={{ color: 'var(--text-secondary)' }}>fg      </span>
              <span style={{ color: 'var(--text)' }}>#e5e5e5</span>
            </div>
            <div style={{ marginBottom: 4 }}>
              <span style={{ color: 'var(--text-secondary)' }}>accent  </span>
              <span style={{ color: 'var(--accent)' }}>#22c55e</span>
            </div>
            <div style={{ marginBottom: 4 }}>
              <span style={{ color: 'var(--text-secondary)' }}>font    </span>
              <span style={{ color: 'var(--text)' }}>JetBrains Mono</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
