/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#080808',
        surface: '#0d0d0d',
        elevated: '#141414',
        border: '#1a1a1a',
        'text-primary': '#e5e5e5',
        'text-secondary': '#8a8a8a',
        'text-muted': '#525252',
        accent: {
          DEFAULT: '#22c55e',
          warning: '#eab308',
          danger: '#ef4444',
          info: '#3b82f6',
        }
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'monospace'],
        sans: ['Inter', 'Sarabun', 'sans-serif'],
      },
      borderRadius: {
        'sm': '4px',
        'md': '6px',
      }
    },
  },
  plugins: [],
}
