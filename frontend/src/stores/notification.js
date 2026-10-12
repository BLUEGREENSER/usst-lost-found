import { defineStore } from 'pinia'
import { unreadCount } from '../api/common'

export const useNotificationStore = defineStore('notification', {
  state: () => ({
    unreadCount: 0,
    timer: null,
  }),
  actions: {
    async fetchUnreadCount() {
      try {
        const res = await unreadCount()
        this.unreadCount = res.data.count
      } catch (e) {}
    },
    startPolling() {
      this.fetchUnreadCount()
      this.timer = setInterval(() => this.fetchUnreadCount(), 60000)
    },
    stopPolling() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
    },
  },
})