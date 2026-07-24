import { useState } from 'react';
import useStore from '../stores/useStore';

export default function LoginBanner() {
  const { login } = useStore();
  const [password, setPassword] = useState('');
  const [loggingIn, setLoggingIn] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!password) return;
    setLoggingIn(true);
    setError('');
    try {
      const ok = await login(password);
      if (!ok) setError('wrong password — try: password');
    } catch {
      setError('backend not reachable — is :8000 running?');
    } finally {
      setLoggingIn(false);
    }
  };

  return (
    <div style={{
      borderBottom: '1px solid #eab308',
      background: 'var(--surface)',
      padding: '12px 16px',
      marginBottom: 8,
    }}>
      <div style={{ color: '#eab308', marginBottom: 4, fontFamily: 'JetBrains Mono, monospace', fontSize: 12 }}>
        {'⚠ not authenticated — enter password to connect'}
      </div>
      <form onSubmit={handleLogin} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
        <span style={{ color: 'var(--text-secondary)', fontFamily: 'JetBrains Mono, monospace', fontSize: 13 }}>{'>'}</span>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="password"
          autoFocus
          style={{
            background: 'transparent',
            border: '1px solid #333',
            color: 'var(--text)',
            fontFamily: 'JetBrains Mono, monospace',
            fontSize: 13,
            padding: '3px 8px',
            outline: 'none',
            width: 200,
          }}
        />
        <button
          type="submit"
          disabled={!password || loggingIn}
          style={{
            background: password ? 'var(--accent)' : '#333',
            color: 'var(--bg)',
            border: 'none',
            padding: '3px 12px',
            fontFamily: 'JetBrains Mono, monospace',
            fontSize: 12,
            cursor: password ? 'pointer' : 'not-allowed',
          }}
        >
          {loggingIn ? '...' : 'connect'}
        </button>
        {error && <span style={{ color: '#ef4444', fontSize: 12, fontFamily: 'JetBrains Mono, monospace' }}>{error}</span>}
      </form>
    </div>
  );
}
