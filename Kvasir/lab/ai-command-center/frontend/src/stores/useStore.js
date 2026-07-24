import { create } from 'zustand';
import * as api from '../api';

const useStore = create((set, get) => ({
  // State
  theme: localStorage.getItem('theme') || 'dark',
  activeTab: 'chat',
  messages: [],
  team: [],
  files: [],
  fileContent: null,
  token: localStorage.getItem('token'),
  isAuthenticated: !!localStorage.getItem('token'),
  loading: false,
  chatLoading: false,
  selectedMember: null,

  // Actions
  setTab: (tab) => set({ activeTab: tab }),

  toggleTheme: () => set((s) => {
    const t = s.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', t);
    return { theme: t };
  }),

  addMessage: (message) =>
    set((s) => ({ messages: [...s.messages, message] })),

  setMessages: (messages) => set({ messages }),

  setLoading: (loading) => set({ loading }),

  setChatLoading: (chatLoading) => set({ chatLoading }),

  setSelectedMember: (member) => set({ selectedMember: member }),

  login: async (password) => {
    try {
      const data = await api.login(password);
      if (data?.token) {
        set({ token: data.token, isAuthenticated: true });
        return true;
      }
      return false;
    } catch {
      return false;
    }
  },

  logout: () => {
    api.logout();
    set({ token: null, isAuthenticated: false, messages: [] });
  },

  fetchTeam: async () => {
    try {
      const data = await api.fetchTeam();
      if (data) set({ team: data });
    } catch (err) {
      console.error('Failed to fetch team:', err);
    }
  },

  fetchFiles: async (path = '') => {
    try {
      const data = await api.fetchFiles(path);
      if (data) set({ files: data.files || data });
    } catch (err) {
      console.error('Failed to fetch files:', err);
    }
  },

  spawnAgent: async (agent, prompt) => {
    try {
      const data = await api.spawnAgent(agent, prompt);
      return data;
    } catch (err) {
      console.error('Failed to spawn agent:', err);
      return null;
    }
  },

  appendToLastMessage: (suffix) =>
    set((s) => {
      const msgs = [...s.messages];
      if (msgs.length > 0) {
        const last = { ...msgs[msgs.length - 1] };
        last.content += suffix;
        msgs[msgs.length - 1] = last;
      }
      return { messages: msgs };
    }),
}));

export default useStore;
