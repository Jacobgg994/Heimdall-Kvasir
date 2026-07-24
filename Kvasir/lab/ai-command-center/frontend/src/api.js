const API_BASE = '/api';

async function request(endpoint, options = {}) {
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const res = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `HTTP ${res.status}`);
  }

  const text = await res.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

export async function chat(prompt) {
  const data = await request('/chat', {
    method: 'POST',
    body: JSON.stringify({ prompt }),
  });
  return data;
}

export async function fetchTeam() {
  return request('/team');
}

export async function fetchFiles(path = '') {
  const params = path ? `?path=${encodeURIComponent(path)}` : '';
  return request(`/files${params}`);
}

export async function spawnAgent(agent, prompt) {
  const data = await request('/agent/spawn', {
    method: 'POST',
    body: JSON.stringify({ agent, prompt }),
  });
  return data;
}

export async function chatStream(prompt, onToken, onDone) {
  const token = localStorage.getItem('token');
  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };
  const response = await fetch('/api/chat/stream', {
    method: 'POST',
    headers,
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  // eslint-disable-next-line no-constant-condition
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || !trimmed.startsWith('data: ')) continue;
      const payload = trimmed.slice(6).trim();
      if (!payload || payload === '[DONE]') continue;
      try {
        const data = JSON.parse(payload);
        if (data.done) {
          if (typeof onDone === 'function') onDone(data.code);
          return;
        }
        if (data.token != null && typeof onToken === 'function') onToken(data.token);
      } catch {
        // skip malformed JSON on this line
      }
    }
  }
  // Stream ended without a done signal — ensure onDone is called
  if (typeof onDone === 'function') onDone();
}

export async function fetchAgentList() {
  return request('/agent/list');
}

export async function login(password) {
  const data = await request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ password }),
  });
  if (data?.token) {
    localStorage.setItem('token', data.token);
  }
  return data;
}

export async function logout() {
  localStorage.removeItem('token');
}

export default {
  chat,
  fetchTeam,
  fetchFiles,
  spawnAgent,
  login,
  logout,
};
