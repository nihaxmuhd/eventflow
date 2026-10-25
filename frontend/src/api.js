import axios from 'axios'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001/api'
const ACCESS_TOKEN_KEY = 'eventflow_access_token'
const REFRESH_TOKEN_KEY = 'eventflow_refresh_token'
const USER_KEY = 'eventflow_user'

export const tokenStore = {
  getAccess: () => localStorage.getItem(ACCESS_TOKEN_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_TOKEN_KEY),
  getUser: () => {
    try { return JSON.parse(localStorage.getItem(USER_KEY)) } catch { return null }
  },
  setSession: ({ access, refresh, user }) => {
    localStorage.setItem(ACCESS_TOKEN_KEY, access)
    localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
    localStorage.setItem(USER_KEY, JSON.stringify(user))
  },
  clear: () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
  },
}

const api = axios.create({ baseURL: API_BASE_URL })

api.interceptors.request.use((config) => {
  const access = tokenStore.getAccess()
  if (access) config.headers.Authorization = `Bearer ${access}`
  return config
})

let refreshRequest

export async function refreshAccessToken() {
  const refresh = tokenStore.getRefresh()
  if (!refresh) return null

  try {
    refreshRequest ||= api.post('/auth/refresh/', { refresh })
    const response = await refreshRequest
    const { access, refresh: nextRefresh } = response.data
    if (!access) return null
    localStorage.setItem(ACCESS_TOKEN_KEY, access)
    if (nextRefresh) localStorage.setItem(REFRESH_TOKEN_KEY, nextRefresh)
    return access
  } catch {
    tokenStore.clear()
    window.dispatchEvent(new Event('eventflow:session-expired'))
    return null
  } finally {
    refreshRequest = undefined
  }
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    const isRefreshRequest = originalRequest?.url?.includes('/auth/refresh/')

    if (error.response?.status !== 401 || originalRequest?._retry || isRefreshRequest) {
      return Promise.reject(error)
    }

    if (!tokenStore.getRefresh()) {
      tokenStore.clear()
      window.dispatchEvent(new Event('eventflow:session-expired'))
      return Promise.reject(error)
    }

    originalRequest._retry = true
    try {
      const access = await refreshAccessToken()
      if (!access) return Promise.reject(error)
      originalRequest.headers.Authorization = `Bearer ${access}`
      return api(originalRequest)
    } catch (refreshError) { return Promise.reject(refreshError) }
  },
)

export default api
