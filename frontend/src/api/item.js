import request from './request'

export const publishLost = (data) => request.post('/lost', data)
export const editLost = (id, data) => request.put(`/lost/${id}`, data)
export const deleteLost = (id) => request.delete(`/lost/${id}`)
export const myLostList = (params) => request.get('/lost/mine', { params })
export const lostDetail = (id) => request.get(`/lost/${id}`)

export const publishFound = (data) => request.post('/found', data)
export const editFound = (id, data) => request.put(`/found/${id}`, data)
export const deleteFound = (id) => request.delete(`/found/${id}`)
export const myFoundList = (params) => request.get('/found/mine', { params })
export const foundDetail = (id) => request.get(`/found/${id}`)