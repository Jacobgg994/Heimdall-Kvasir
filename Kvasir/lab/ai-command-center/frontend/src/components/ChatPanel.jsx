import { useState, useRef, useEffect, useCallback } from 'react';
import useStore from '../stores/useStore';
import { chatStream, spawnAgent, fetchTeam } from '../api';
import LoginBanner from './LoginBanner';

const MAX_HISTORY = 50;
const CMD_HISTORY_KEY = 'cmd_history';

// Fallback team list for autocomplete
const TEAM_MEMBERS = [
  { id: 'gemmy', emoji: '💎', name: 'GEMMY' },
  { id: 'jasper', emoji: '🔭', name: 'JASPER' },
  { id: 'komhas', emoji: '📈', name: 'KOMHAS' },
  { id: 'cila', emoji: '🤝', name: 'CILA' },
  { id: 'kamu', emoji: '🦅', name: 'KAMU' },
  { id: 'salmon', emoji: '🎨', name: 'SALMON' },
  { id: 'pyke', emoji: '🐟', name: 'PYKE' },
  { id: 'canvas', emoji: '🎨', name: 'CANVAS' },
  { id: 'jimmy', emoji: '🌊', name: 'JIMMY' },
  { id: 'zara', emoji: '⚡', name: 'ZARA' },
  { id: 'orion', emoji: '⭐', name: 'ORION' },
  { id: 'nova', emoji: '🌙', name: 'NOVA' },
  { id: 'echo', emoji: '🔊', name: 'ECHO' },
  { id: 'forge', emoji: '🔨', name: 'FORGE' },
  { id: 'pixel', emoji: '🎮', name: 'PIXEL' },
  { id: 'drift', emoji: '🌊', name: 'DRIFT' },
  { id: 'spark', emoji: '✨', name: 'SPARK' },
  { id: 'frost', emoji: '❄️', name: 'FROST' },
  { id: 'blaze', emoji: '🔥', name: 'BLAZE' },
  { id: 'sage', emoji: '🌿', name: 'SAGE' },
  { id: 'flux', emoji: '🌀', name: 'FLUX' },
  { id: 'ember', emoji: '💫', name: 'EMBER' },
  { id: 'stone', emoji: '🪨', name: 'STONE' },
];

function loadHistory() {
  try {
    const raw = localStorage.getItem(CMD_HISTORY_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

function saveHistory(history) {
  try {
    localStorage.setItem(CMD_HISTORY_KEY, JSON.stringify(history));
  } catch {
    // storage full or unavailable
  }
}

function ChatMessage({ msg }) {
  const isUser = msg.role === 'user';
  const isSystem = msg.role === 'system';

  let prefix = '';
  let color = 'var(--text)';
  if (isSystem) {
    prefix = '# ';
    color = 'var(--text-secondary)';
  } else if (isUser) {
    prefix = '> ';
    color = 'var(--accent)';
  } else {
    prefix = '  ';
    color = 'var(--text)';
  }

  return (
    <div className="message-line" style={{ marginBottom: 4 }}>
      <span style={{ color: isUser ? 'var(--accent)' : isSystem ? 'var(--text-secondary)' : 'var(--text)' }}>
        {prefix}
      </span>
      <span style={{ color, whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
        {msg.content}
      </span>
    </div>
  );
}

export default function ChatPanel() {
  const [input, setInput] = useState('');
  const [cmdHistory, setCmdHistory] = useState(loadHistory);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [showMention, setShowMention] = useState(false);
  const [mentionFilter, setMentionFilter] = useState('');
  const [mentionStart, setMentionStart] = useState(0);
  const [mentionIndex, setMentionIndex] = useState(0);
  const [teamList, setTeamList] = useState(TEAM_MEMBERS);

  const { messages, addMessage, setMessages, chatLoading, setChatLoading, appendToLastMessage, activeTab, isAuthenticated } = useStore();
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const containerRef = useRef(null);

  // Load team list from API on mount
  useEffect(() => {
    (async () => {
      try {
        const data = await fetchTeam();
        if (data && data.length > 0) {
          setTeamList(data);
        }
      } catch {
        // use fallback
      }
    })();
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'auto' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, chatLoading]);

  useEffect(() => {
    if (activeTab === 'chat') {
      setTimeout(() => inputRef.current?.focus(), 50);
    }
  }, [activeTab]);

  // --- Command History ---
  const addToHistory = useCallback((cmd) => {
    setCmdHistory((prev) => {
      if (prev[prev.length - 1] === cmd) return prev;
      const next = [...prev, cmd];
      if (next.length > MAX_HISTORY) next.shift();
      saveHistory(next);
      return next;
    });
    setHistoryIndex(-1);
  }, []);

  // --- @Mention Autocomplete ---
  const filteredMembers = showMention
    ? teamList.filter((m) =>
        m.id.toLowerCase().includes(mentionFilter.toLowerCase()) ||
        m.name.toLowerCase().includes(mentionFilter.toLowerCase())
      )
    : [];

  const parseMention = useCallback((value) => {
    const lastAtIndex = value.lastIndexOf('@');
    if (lastAtIndex !== -1 && (lastAtIndex === 0 || value[lastAtIndex - 1] === ' ')) {
      const afterAt = value.slice(lastAtIndex + 1);
      const spaceAt = afterAt.indexOf(' ');
      const filterText = spaceAt === -1 ? afterAt : afterAt.slice(0, spaceAt);
      setMentionFilter(filterText);
      setMentionStart(lastAtIndex);
      setMentionIndex(0);
      setShowMention(true);
    } else {
      setShowMention(false);
    }
  }, []);

  const completeMention = useCallback((member) => {
    const beforeAt = input.slice(0, mentionStart);
    const rest = input.slice(mentionStart);
    const spaceIdx = rest.indexOf(' ', 1);
    const afterMention = spaceIdx === -1 ? '' : rest.slice(spaceIdx);
    const newInput = beforeAt + '@' + member.id + ' ' + afterMention;
    setInput(newInput);
    setShowMention(false);
    inputRef.current?.focus();
  }, [input, mentionStart]);

  // --- Clear Command ---
  const handleClear = useCallback(() => {
    setMessages([]);
    addMessage({ role: 'system', content: 'Screen cleared.' });
  }, [setMessages, addMessage]);

  // --- @Agent Spawn ---
  const handleAgentSpawn = useCallback(async (agentName, agentPrompt) => {
    setChatLoading(true);
    addMessage({ role: 'system', content: `\u{1F527} Spawning @${agentName}...` });
    try {
      const result = await spawnAgent(agentName, agentPrompt);
      const resultStr = typeof result === 'string' ? result : JSON.stringify(result, null, 2);
      addMessage({ role: 'system', content: `✅ @${agentName} completed:\n${resultStr}` });
    } catch (err) {
      addMessage({ role: 'system', content: `❌ @${agentName} error: ${err.message}` });
    } finally {
      setChatLoading(false);
    }
  }, [addMessage, setChatLoading]);

  // --- Send / Stream ---
  const handleSend = useCallback(async () => {
    const prompt = input.trim();
    if (!prompt || chatLoading) return;

    // Save to history
    addToHistory(prompt);

    // Check for @agentname spawn pattern: @agent prompt
    const spawnMatch = prompt.match(/^@(\w+)\s+(.+)/);
    if (spawnMatch) {
      setInput('');
      addMessage({ role: 'user', content: prompt });
      await handleAgentSpawn(spawnMatch[1].toLowerCase(), spawnMatch[2]);
      return;
    }

    // Check for clear command
    if (prompt === 'clear') {
      setInput('');
      handleClear();
      return;
    }

    // Normal chat with streaming
    setInput('');
    addMessage({ role: 'user', content: prompt });
    setChatLoading(true);

    // Add placeholder assistant message
    addMessage({ role: 'assistant', content: '' });

    try {
      await chatStream(
        prompt,
        (token) => {
          appendToLastMessage(token);
        },
        () => {
          setChatLoading(false);
        }
      );
    } catch (err) {
      setChatLoading(false);
      // Remove the empty assistant message if stream failed before any content
      const msgs = useStore.getState().messages;
      const lastMsg = msgs[msgs.length - 1];
      if (lastMsg && lastMsg.role === 'assistant' && lastMsg.content === '') {
        useStore.getState().setMessages(msgs.slice(0, -1));
      }
      addMessage({ role: 'system', content: `Error: ${err.message}` });
    }
  }, [input, chatLoading, addToHistory, addMessage, handleClear, handleAgentSpawn, appendToLastMessage, setChatLoading]);

  // --- Input handlers ---
  const handleInputChange = (e) => {
    const value = e.target.value;
    setInput(value);
    parseMention(value);
  };

  const handleKeyDown = (e) => {
    // Tab: complete mention
    if (e.key === 'Tab' && showMention && filteredMembers.length > 0) {
      e.preventDefault();
      completeMention(filteredMembers[mentionIndex] || filteredMembers[0]);
      return;
    }

    // Escape: close mention dropdown
    if (e.key === 'Escape') {
      if (showMention) {
        e.preventDefault();
        setShowMention(false);
        return;
      }
    }

    // ArrowDown: navigate mention dropdown or history forward
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (showMention && filteredMembers.length > 0) {
        setMentionIndex((prev) => Math.min(prev + 1, filteredMembers.length - 1));
        return;
      }
      // Command history forward
      if (historyIndex === -1) return;
      const newIdx = Math.min(historyIndex + 1, cmdHistory.length - 1);
      setHistoryIndex(newIdx);
      setInput(cmdHistory[newIdx] || '');
      return;
    }

    // ArrowUp: navigate mention dropdown or history back
    if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (showMention && filteredMembers.length > 0) {
        setMentionIndex((prev) => Math.max(prev - 1, 0));
        return;
      }
      // Command history back
      if (cmdHistory.length === 0) return;
      const newIdx = historyIndex === -1 ? cmdHistory.length - 1 : Math.max(historyIndex - 1, 0);
      setHistoryIndex(newIdx);
      setInput(cmdHistory[newIdx]);
      return;
    }

    // Enter: send or complete mention
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (showMention && filteredMembers.length > 0) {
        completeMention(filteredMembers[mentionIndex] || filteredMembers[0]);
        return;
      }
      handleSend();
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      background: 'var(--bg)',
    }}>
      {/* Messages area */}
      <div
        ref={containerRef}
        className="chat-messages"
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '12px 16px',
          fontFamily: 'JetBrains Mono, monospace',
          fontSize: 13,
          lineHeight: 1.6,
        }}
      >
        {/* Login prompt */}
        {!isAuthenticated && <LoginBanner />}

        {/* Welcome message */}
        {isAuthenticated && messages.length === 0 && (
          <div style={{ marginBottom: 16 }}>
            <div style={{ color: 'var(--accent)', marginBottom: 8 }}>
              {'# JACOB Command Center v1.1'}
            </div>
            <div style={{ color: 'var(--text-secondary)', marginBottom: 4 }}>
              {'# connected · localhost:8000 · 22 agents ready'}
            </div>
            <div style={{ color: 'var(--text-secondary)', marginBottom: 4 }}>
              {'# type a command to talk to JIMMY'}
            </div>
            <div style={{ color: 'var(--text-secondary)', marginBottom: 4 }}>
              {'# @agentname <prompt> to spawn an agent'}
            </div>
            <div style={{ color: 'var(--text-secondary)' }}>
              {'# type "clear" to clear screen'}
            </div>
            <div style={{ color: 'var(--text-secondary)' }}>{'#'}</div>
          </div>
        )}

        {messages.map((msg, idx) => (
          <ChatMessage key={idx} msg={msg} />
        ))}

        {/* Loading / streaming indicator */}
        {chatLoading && (
          <div className="message-line" style={{ marginBottom: 4 }}>
            <span className="streaming-cursor">{'  ▌'}</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="chat-input-area" style={{
        borderTop: '1px solid var(--border)',
        padding: '8px 16px 10px',
        background: 'var(--bg)',
        position: 'relative',
      }}>
        {/* @mention dropdown */}
        {showMention && filteredMembers.length > 0 && (
          <div style={{
            position: 'absolute',
            bottom: '100%',
            left: 24,
            right: 16,
            maxHeight: 220,
            overflowY: 'auto',
            background: '#111',
            border: '1px solid #333',
            borderBottom: 'none',
            borderRadius: '4px 4px 0 0',
            fontFamily: 'JetBrains Mono, monospace',
            fontSize: 13,
            zIndex: 100,
          }}>
            {filteredMembers.map((member, idx) => (
              <div
                key={member.id}
                onClick={() => completeMention(member)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  padding: '6px 12px',
                  cursor: 'pointer',
                  background: idx === mentionIndex ? '#1a3a1a' : 'transparent',
                  color: idx === mentionIndex ? 'var(--accent)' : 'var(--text)',
                }}
              >
                <span>{member.emoji}</span>
                <span style={{ fontWeight: 500 }}>{member.name}</span>
                <span style={{ color: 'var(--text-secondary)', fontSize: 11 }}>@{member.id}</span>
              </div>
            ))}
          </div>
        )}

        <div style={{ display: 'flex', alignItems: 'center', gap: 0 }}>
          <span style={{ color: 'var(--accent)', fontFamily: 'JetBrains Mono, monospace', fontSize: 13, marginRight: 8 }}>
            {'> '}
          </span>
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="type a command... (@ for agents)"
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
          {input.length === 0 && !chatLoading && (
            <span className="cursor" style={{ color: 'var(--accent)', fontSize: 13 }} />
          )}
        </div>
      </div>
    </div>
  );
}
