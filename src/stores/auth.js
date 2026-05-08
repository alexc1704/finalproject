import { defineStore } from 'pinia'
import { apiFetch } from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('dd_user') || 'null'),
    isLoggedIn: Boolean(localStorage.getItem('dd_user'))
  }),
  getters: {
    userId: (state) => state.user?.id || null,
    profile: (state) => state.user?.profile || null
  },
  actions: {
    setUser(user) {
      this.user = user
      this.isLoggedIn = Boolean(user)
      if (user) localStorage.setItem('dd_user', JSON.stringify(user))
      else localStorage.removeItem('dd_user')
    },
    async login(email, password) {
      const data = await apiFetch('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password })
      })
      this.setUser(data.user)
      return data.user
    },
    async register(payload) {
      const data = await apiFetch('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify(payload)
      })
      this.setUser(data.user)
      return data.user
    },
    async loadMe() {
      const data = await apiFetch('/api/auth/me')
      this.setUser(data.user)
      return data.user
    },
    async logout() {
      try { await apiFetch('/api/auth/logout', { method: 'POST' }) } catch (e) {}
      this.setUser(null)
    },
    refreshProfile(profile) {
      if (this.user) this.setUser({ ...this.user, profile })
    }
  }
})
