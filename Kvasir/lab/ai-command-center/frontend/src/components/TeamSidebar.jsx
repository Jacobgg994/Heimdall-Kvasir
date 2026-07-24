import { useState, useEffect } from 'react';
import { fetchTeam } from '../api';

const TEAM_MEMBERS = [
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

const STATUS_DOT_ONLINE = { color: '#22c55e', symbol: '●' };
const STATUS_DOT_IDLE = { color: '#666', symbol: '○' };

export default function TeamSidebar() {
  const [members, setMembers] = useState(TEAM_MEMBERS);
  const [selected, setSelected] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const data = await fetchTeam();
        if (data && data.length > 0) {
          // Merge API data with defaults to preserve emoji/name/role
          const merged = TEAM_MEMBERS.map((def) => {
            const api = data.find((d) => d.id === def.id);
            return api ? { ...def, ...api } : def;
          });
          setMembers(merged);
        }
      } catch {
        // keep defaults
      }
    })();
  }, []);

  const getStatusDot = (member) => {
    if (!member.status || member.status === 'online' || member.status === 'ready') {
      return STATUS_DOT_ONLINE;
    }
    return STATUS_DOT_IDLE;
  };

  return (
    <div
      style={{
        width: 240,
        flexShrink: 0,
        background: 'var(--surface)',
        borderLeft: '1px solid var(--border)',
        display: 'flex',
        flexDirection: 'column',
        fontFamily: 'JetBrains Mono, monospace',
        overflow: 'hidden',
      }}
    >
      {/* Header */}
      <div
        style={{
          padding: '8px 12px',
          borderBottom: '1px solid var(--border)',
          fontSize: 11,
          fontWeight: 600,
          color: 'var(--accent)',
          letterSpacing: 1.5,
          flexShrink: 0,
        }}
      >
        TEAM ({members.length})
      </div>

      {/* Member list */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '4px 0' }}>
        {members.map((member) => {
          const dot = getStatusDot(member);
          const isSelected = selected === member.id;
          return (
            <div
              key={member.id}
              onClick={() => setSelected(isSelected ? null : member.id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 6,
                padding: '3px 12px',
                fontSize: 11,
                lineHeight: '20px',
                cursor: 'pointer',
                background: isSelected ? 'var(--border)' : 'transparent',
                color: isSelected ? 'var(--accent)' : 'var(--text)',
                transition: 'none',
                userSelect: 'none',
              }}
            >
              <span style={{ color: dot.color, fontSize: 10, width: 10, display: 'inline-block' }}>
                {dot.symbol}
              </span>
              <span style={{ fontSize: 12 }}>{member.emoji}</span>
              <span
                style={{
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                }}
              >
                {member.name}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
