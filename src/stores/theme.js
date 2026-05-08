import { defineStore } from 'pinia'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    mode: localStorage.getItem('dd_theme') || 'light'
  }),
  actions: {
    apply() {
      document.documentElement.setAttribute('data-theme', this.mode)
      localStorage.setItem('dd_theme', this.mode)
    },
    toggle() {
      this.mode = this.mode === 'dark' ? 'light' : 'dark'
      this.apply()
    },
    setMode(mode) {
      this.mode = mode
      this.apply()
    }
  }
})
