// 全局后端地址配置
// VITE_API_BASE: 后端 API 根地址（不含 /api/v1），用于 GitHub Pages 等跨域部署场景
export const API_BASE = import.meta.env.VITE_API_BASE || ''

// 后端完整 URL（含协议和域名），用于拼接图片等资源地址
export const BACKEND_ORIGIN = API_BASE

// 解析图片 URL：把后端返回的相对路径（如 /static/uploads/x.jpg）拼上后端域名
export function resolveImageUrl(url) {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('data:')) {
    return url
  }
  return API_BASE + url
}

// 批量解析图片 URL 列表
export function resolveImageUrls(urls) {
  if (!urls || !urls.length) return []
  return urls.map(resolveImageUrl)
}

export default API_BASE
