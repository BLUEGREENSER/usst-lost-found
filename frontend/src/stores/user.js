import { defineStore } from 'pinia'
import { login as apiLogin, logout as apiLogout } from '../api/auth'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || 'null'),
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
    isAdmin: (state) => state.userInfo?.role === 'admin',
  },
  actions: {
    async login(account, password) {
      const res = await apiLogin({ account, password })
      this.token = res.data.token
      this.userInfo = res.data.user
      localStorage.setItem('token', this.token)
      localStorage.setItem('role', res.data.user.role)
      localStorage.setItem('userInfo', JSON.stringify(this.userInfo))
      return res
    },
    async logout() {
      try { await apiLogout() } catch (e) {}
      this.token = ''
      this.userInfo = null
      localStorage.removeItem('token')
      localStorage.removeItem('role')
      localStorage.removeItem('userInfo')
    },
  },
})