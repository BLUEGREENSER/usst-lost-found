import request from './request'

export const listMatches = (params) => request.get('/matches', { params })
export const confirmMatch = (id) => request.post(`/matches/${id}/confirm`)
export const rejectMatch = (id) => request.post(`/matches/${id}/reject`)

export const createClaim = (data) => request.post('/claims', data)
export const verifyClaim = (id, data) => request.post(`/claims/${id}/verify`, data)
export const cancelClaim = (id) => request.post(`/claims/${id}/cancel`)
export const resendCode = (id) => request.post(`/claims/${id}/resend`)
export const claimDetail = (id) => request.get(`/claims/${id}`)

export const search = (params) => request.get('/search', { params })

export const listNotifications = (params) => request.get('/notifications', { params })
export const unreadCount = () => request.get('/notifications/unread-count')
export const markRead = (id) => request.post(`/notifications/${id}/read`)
export const markAllRead = () => request.post('/notifications/read-all')

export const uploadImage = (formData) => request.post('/upload/image', formData, {
  headers: { 'Content-Type': 'multipart/form-data' },
})

export const auditList = (params) => request.get('/admin/audit/list', { params })
export const approve = (type, id) => request.post(`/admin/audit/${type}/${id}/approve`)
export const reject = (type, id, data) => request.post(`/admin/audit/${type}/${id}/reject`, data)
export const takedown = (type, id, data) => request.post(`/admin/items/${type}/${id}/takedown`, data)
export const listUsers = (params) => request.get('/admin/users', { params })
export const enableUser = (id) => request.post(`/admin/users/${id}/enable`)
export const disableUser = (id) => request.post(`/admin/users/${id}/disable`)
export const stats = (params) => request.get('/admin/stats', { params })