import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const request = axios.create({
  // 后端 API 地址：可通过环境变量 VITE_API_BASE 覆盖（用于公网后端），默认同源
  baseURL: import.meta.env.VITE_API_BASE || '/api/v1',
  timeout: 10000,
})

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res.code === 0) {
      return res
    }
    if (res.code === 10002) {
      localStorage.removeItem('token')
      router.push('/login')
      ElMessage.error('登录已过期，请重新登录')
    } else if (res.code === 10003) {
      ElMessage.error(res.message || '无权限')
    } else {
      ElMessage.error(res.message || '请求失败')
    }
    return Promise.reject(res)
  },
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      router.push('/login')
    }
    ElMessage.error(error.message || '网络错误')
    return Promise.reject(error)
  }
)

export default request