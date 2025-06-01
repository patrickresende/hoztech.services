/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './core/templates/**/*.html',
    './core/static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        'neon-blue': '#00f7ff',
        'neon-purple': '#9d00ff',
        'neon-green': '#00ff9d',
        'cyber-dark': '#0a0b1e',
        'cyber-dark-soft': 'rgba(10, 11, 30, 0.95)',
        'cyber-grid': '#1a1b3d',
        'cyber-text': '#e0fbfc',
        'success-cyber': '#00ff9d',
        'danger-cyber': '#ff073a',
      },
      boxShadow: {
        'neon-blue': '0 0 20px rgba(0, 247, 255, 0.3)',
        'neon-purple': '0 0 20px rgba(157, 0, 255, 0.3)',
        'neon-green': '0 0 20px rgba(0, 255, 157, 0.3)',
      },
      animation: {
        'pulse-neon': 'pulse-neon 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'grid-move': 'grid-move 20s linear infinite',
        'fade-in': 'fadeIn 0.5s ease-out forwards',
        'slide-up': 'slideUp 0.5s ease-out forwards',
        'glow': 'glow 2s ease-in-out infinite',
      },
      keyframes: {
        'pulse-neon': {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.5 },
        },
        'grid-move': {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(50px)' },
        },
        'fadeIn': {
          '0%': { opacity: 0, transform: 'scale(0.95)' },
          '100%': { opacity: 1, transform: 'scale(1)' },
        },
        'slideUp': {
          '0%': { opacity: 0, transform: 'translateY(20px)' },
          '100%': { opacity: 1, transform: 'translateY(0)' },
        },
        'glow': {
          '0%, 100%': { textShadow: '0 0 10px rgba(0, 247, 255, 0.3)' },
          '50%': { textShadow: '0 0 20px rgba(0, 247, 255, 0.6)' },
        },
      },
      textShadow: {
        'neon': '0 0 10px rgba(0, 247, 255, 0.3), 0 0 20px rgba(0, 247, 255, 0.3)',
      },
      backgroundImage: {
        'grid': 'linear-gradient(90deg, var(--cyber-grid) 1px, transparent 1px), linear-gradient(0deg, var(--cyber-grid) 1px, transparent 1px)',
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      },
      transitionDuration: {
        '2000': '2000ms',
      },
      scale: {
        '102': '1.02',
      },
    },
  },
  plugins: [
    // Plugin para text-shadow (opcional, você pode criar manualmente também)
    function({ addUtilities }) {
      const newUtilities = {
        '.text-shadow-neon': {
          textShadow: '0 0 10px rgba(0, 247, 255, 0.3), 0 0 20px rgba(0, 247, 255, 0.3)',
        },
      }
      addUtilities(newUtilities)
    },
  ],
} 