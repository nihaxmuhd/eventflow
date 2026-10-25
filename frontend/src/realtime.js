import { API_BASE_URL, refreshAccessToken, tokenStore } from './api'
export { isRealtimeEvent } from './realtimeEvent'
import { isRealtimeEvent } from './realtimeEvent'
const MAX_RECONNECT_ATTEMPTS = 5

function websocketUrl() {
  const url = new URL(API_BASE_URL, window.location.origin)
  url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
  url.pathname = '/ws/events/'
  url.search = ''
  return url.toString()
}

class RealtimeClient {
  constructor() {
    this.socket = null
    this.listeners = new Set()
    this.reconnectTimer = null
    this.reconnectAttempts = 0
    this.closedByClient = false
    this.refreshing = false
  }

  subscribe(listener) {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  connect() {
    if (this.socket || !tokenStore.getAccess()) return
    this.closedByClient = false
    const socket = new WebSocket(websocketUrl())
    this.socket = socket
    socket.onmessage = (message) => this.handleMessage(message, socket)
    socket.onclose = (event) => this.handleClose(event, socket)
    socket.onerror = () => { /* close drives bounded reconnects */ }
  }

  disconnect() {
    this.closedByClient = true
    window.clearTimeout(this.reconnectTimer)
    this.reconnectTimer = null
    const socket = this.socket
    this.socket = null
    if (socket && socket.readyState < WebSocket.CLOSING) socket.close()
  }

  handleMessage(message, socket) {
    let data
    try { data = JSON.parse(message.data) } catch { return }
    if (data?.type === 'auth.required') {
      const token = tokenStore.getAccess()
      if (token && socket.readyState === WebSocket.OPEN) socket.send(JSON.stringify({ type: 'auth', token }))
      return
    }
    if (data?.type === 'auth.success') {
      this.reconnectAttempts = 0
      return
    }
    if (isRealtimeEvent(data)) this.listeners.forEach((listener) => listener(data.event))
  }

  async handleClose(event, socket) {
    if (this.socket !== socket) return
    this.socket = null
    if (this.closedByClient || !tokenStore.getAccess()) return
    if (event.code === 4401 && !this.refreshing) {
      this.refreshing = true
      await refreshAccessToken()
      this.refreshing = false
    }
    if (!tokenStore.getAccess() || this.reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) return
    const delay = Math.min(1000 * 2 ** this.reconnectAttempts, 16000)
    this.reconnectAttempts += 1
    this.reconnectTimer = window.setTimeout(() => this.connect(), delay)
  }
}

export const realtimeClient = new RealtimeClient()
