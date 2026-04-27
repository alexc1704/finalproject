import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isLoggedIn: false
  }),
  actions: {
    login(userData, token) {
      this.user = userData
      this.token = token
      this.isLoggedIn = true
    },
    logout() {
      this.user = null
      this.token = null
      this.isLoggedIn = false
    }
  }
})