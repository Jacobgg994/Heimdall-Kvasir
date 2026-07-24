import { useState, useEffect } from 'react';
import useStore from '../stores/useStore';
import { fetchTeam } from '../api';

const teamMembers = [
  { id: 'gemmy', emoji: '💎', name: 'GEMMY', role: 'GemLogin & Phone Farm Expert' },
  { id: 'jasper', emoji: '🔭', name: 'JASPER', role: 'Trend Scout' },
  { id: 'komhas', emoji: '📈', name: 'KOMHAS', role: 'Digital Marketing' },
  { id: 'cila', emoji: '🤝', name: 'CILA', role: 'HR & People' },
  { id: 'kamu', emoji: '🦅', name: 'KAMU', role: 'Sales & Partnership' },
  { id: 'salmon', emoji: '🎨', name: 'SALMON', role: 'Content Creator' },
  { id: 'pyke', emoji: '🐟', name: 'PYKE', role: 'Frontend Architect' },
  { id: 'canvas', emoji: '🎨', name: 'CANVAS', role: 'UI/UX Designer' },
  { id: 'jimmy', emoji: '🌊', name: 'JIMMY', role: 'Ocean Kvasir' },
  { id: 'zara', emoji: '⚡', name: 'ZARA', role: 'Automation Specialist' },
  { id: 'orion', emoji: '⭐', name: 'ORION', role: 'Data Analyst' },
  { id: 'nova', emoji: '🌙', name: 'NOVA', role: 'Research Assistant' },
  { id: 'echo', emoji: '🔊', name: 'ECHO', role: 'Communications' },
  { id: 'forge', emoji: '🔨', name: 'FORGE', role: 'Infrastructure' },
  { id: 'pixel', emoji: '🎮', name: 'PIXEL', role: 'Game Dev' },
  { id: 'drift', emoji: '🌊', name: 'DRIFT', role: 'Security' },
  { id: 'spark', emoji: '✨', name: 'SPARK', role: 'Creative Director' },
  { id: 'frost', emoji: '❄️', name: 'FROST', role: 'Backend Engineer' },
  { id: 'blaze', emoji: '🔥', name: 'BLAZE', role: 'DevOps' },
  { id: 'sage', emoji: '🌿', name: 'SAGE', role: 'Strategy' },
  { id: 'flux', emoji: '🌀', name: 'FLUX', role: 'Full Stack' },
  { id: 'ember', emoji: '💫', name: 'EMBER', role: 'Design Lead' },
  { id: 'stone', emoji: '🪨', name: 'STONE', role: 'QA & Testing' },
];

export default function TeamPanel() {
  const [search, setSearch] = useState('');
  const [localTeam, setLocalTeam] = useState(teamMembers);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTeam();
  }, []);

  const loadTeam = async () => {
    setLoading(true);
    try {
      const data = await fetchTeam();
      if (data && data.length > 0) {
        setLocalTeam(data);
      }
    } catch {
      // Use default team
    } finally {
      setLoading(false);
    }
  };

  const filtered = localTeam.filter(
    (m) =>
      m.name.toLowerCase().includes(search.toLowerCase()) ||
      m.role.toLowerCase().includes(search.toLowerCase())
  );

  const handleSendTask = (member) => {
    useStore.getState().setTab('chat');
    useStore.getState().addMessage({
      role: 'user',
      content: `Send task to ${member.name}: `
    });
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
      {/* Header bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '8px 16px',
        borderBottom: '1px solid var(--border)',
        background: 'var(--bg)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ color: 'var(--accent)' }}>$</span>
          <span style={{ color: 'var(--text-secondary)' }}>team --list</span>
          <span style={{ color: 'var(--text-secondary)', fontSize: 11 }}>({localTeam.length} members)</span>
        </div>
        <button
          onClick={loadTeam}
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

      {/* Search */}
      <div style={{
        padding: '8px 16px',
        borderBottom: '1px solid var(--border)',
        display: 'flex',
        alignItems: 'center',
        gap: 8,
      }}>
        <span style={{ color: 'var(--text-secondary)' }}>$</span>
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="grep ..."
          style={{
            flex: 1,
            background: 'transparent',
            border: 'none',
            color: 'var(--text)',
            fontFamily: 'JetBrains Mono, monospace',
            fontSize: 13,
            outline: 'none',
            padding: '2px 0',
          }}
        />
      </div>

      {/* List */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '4px 0' }}>
        {loading ? (
          <div style={{ padding: '16px', color: 'var(--text-secondary)', textAlign: 'center' }}>loading...</div>
        ) : (
          filtered.map((member) => (
            <div
              key={member.id}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                padding: '6px 16px',
                borderBottom: '1px solid #111',
                cursor: 'default',
              }}
            >
              <span style={{ color: 'var(--accent)', fontSize: 10 }}>●</span>
              <span style={{ width: 20, textAlign: 'center' }}>{member.emoji}</span>
              <span style={{ color: 'var(--text)', fontWeight: 500, minWidth: 80 }}>{member.name}</span>
              <span style={{ color: 'var(--text-secondary)', flex: 1 }}>{member.role}</span>
              <button
                onClick={() => handleSendTask(member)}
                style={{
                  background: 'transparent',
                  color: '#3b82f6',
                  border: '1px solid #333',
                  padding: '1px 6px',
                  fontSize: 10,
                  fontFamily: 'JetBrains Mono, monospace',
                  cursor: 'pointer',
                }}
              >
                task
              </button>
            </div>
          ))
        )}

        {filtered.length === 0 && !loading && (
          <div style={{ padding: '16px', color: 'var(--text-secondary)', textAlign: 'center' }}>
            no matches for "{search}"
          </div>
        )}
      </div>

      {/* Status bar */}
      <div style={{
        padding: '4px 16px',
        borderTop: '1px solid var(--border)',
        color: '#555',
        fontSize: 11,
        display: 'flex',
        justifyContent: 'space-between',
      }}>
        <span>{filtered.length} of {localTeam.length}</span>
        <span>agents ready</span>
      </div>
    </div>
  );
}
