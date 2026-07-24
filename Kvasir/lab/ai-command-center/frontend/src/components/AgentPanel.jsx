import { useState, useEffect, useCallback } from 'react';
import { fetchAgentList } from '../api';

export default function AgentPanel() {
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);

  const loadAgents = useCallback(async () => {
    try {
      const data = await fetchAgentList();
      setAgents(data || []);
    } catch {
      setAgents([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadAgents();
    const interval = setInterval(loadAgents, 3000);
    return () => clearInterval(interval);
  }, [loadAgents]);

  const handleKill = async (pid) => {
    try {
      const token = localStorage.getItem('token');
      await fetch('/api/agent/kill', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ pid }),
      });
      loadAgents();
    } catch (err) {
      console.error('Failed to kill agent:', err);
    }
  };

  const formatTime = (seconds) => {
    if (!seconds && seconds !== 0) return '-';
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}m ${s}s`;
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
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '8px 16px',
        borderBottom: '1px solid var(--border)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ color: 'var(--accent)' }}>$</span>
          <span style={{ color: 'var(--text-secondary)' }}>ps aux | grep agent</span>
        </div>
        <button
          onClick={loadAgents}
          style={{
            background: 'transparent',
            color: 'var(--text-secondary)',
            border: '1px solid #333',
            padding: '2px 8px',
            fontSize: 11,
            fontFamily: 'JetBrains Mono, monospace',
            cursor: 'pointer',
          }}
        >
          refresh
        </button>
      </div>

      {/* List */}
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {loading ? (
          <div style={{ padding: '24px', color: 'var(--text-secondary)', textAlign: 'center' }}>loading...</div>
        ) : agents.length === 0 ? (
          <div style={{ padding: '24px', color: 'var(--text-secondary)', textAlign: 'center' }}>
            <div style={{ marginBottom: 8 }}>no running agents</div>
            <div style={{ color: '#555', fontSize: 11 }}>spawn agents from chat using @agentname</div>
          </div>
        ) : (
          agents.map((agent, i) => (
            <div
              key={agent.pid || i}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                padding: '8px 16px',
                borderBottom: '1px solid #111',
              }}
            >
              <span style={{
                color: agent.status === 'running' ? 'var(--accent)' : 'var(--text-secondary)',
                fontSize: 10,
              }}>
                ●
              </span>
              <span style={{ width: 24, textAlign: 'center' }}>{agent.emoji || '🤖'}</span>
              <span style={{ color: 'var(--text)', fontWeight: 500, minWidth: 80 }}>
                {agent.name}
              </span>
              <span style={{ color: 'var(--text-secondary)', minWidth: 70 }}>
                PID {agent.pid}
              </span>
              <span style={{ color: 'var(--text-secondary)', minWidth: 60 }}>
                {formatTime(agent.running_time)}
              </span>
              <span style={{
                color: agent.status === 'running' ? 'var(--accent)' : '#f59e0b',
                fontSize: 11,
                minWidth: 50,
              }}>
                {agent.status}
              </span>
              <div style={{ flex: 1 }} />
              <button
                onClick={() => handleKill(agent.pid)}
                style={{
                  background: 'transparent',
                  color: '#ef4444',
                  border: '1px solid #333',
                  padding: '2px 8px',
                  fontSize: 11,
                  fontFamily: 'JetBrains Mono, monospace',
                  cursor: 'pointer',
                }}
              >
                kill
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
