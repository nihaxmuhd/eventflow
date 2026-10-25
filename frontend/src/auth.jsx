import { createContext, useContext, useEffect, useMemo, useState } from 'react'
import api, { tokenStore } from './api'
import { realtimeClient } from './realtime'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(tokenStore.getUser())
  const [isRestoring, setIsRestoring] = useState(true)

  useEffect(() => {
    const restoreSession = async () => {
      if (!tokenStore.getAccess()) {
        setIsRestoring(false)
        return
      }

      try {
        const response = await api.get('/auth/me/')
        const currentUser = response.data.data
        localStorage.setItem('eventflow_user', JSON.stringify(currentUser))
        setUser(currentUser)
      } catch {
        tokenStore.clear()
        setUser(null)
      } finally {
        setIsRestoring(false)
      }
    }

    const handleExpiredSession = () => setUser(null)
    window.addEventListener('eventflow:session-expired', handleExpiredSession)
    restoreSession()
    return () => window.removeEventListener('eventflow:session-expired', handleExpiredSession)
  }, [])

  useEffect(() => {
    if (!user) {
      realtimeClient.disconnect()
      return undefined
    }
    realtimeClient.connect()
    return () => realtimeClient.disconnect()
  }, [user])

  const login = async (login, password) => {
    const response = await api.post('/auth/login/', { login, password })
    const session = response.data.data
    tokenStore.setSession(session)
    setUser(session.user)
    return session.user
  }

  const logout = async () => {
    const refresh = tokenStore.getRefresh()
    try {
      if (refresh) await api.post('/auth/logout/', { refresh })
    } catch {
      // Local logout still completes if the backend session has already expired.
    } finally {
      tokenStore.clear()
      setUser(null)
    }
  }

  const value = useMemo(() => ({ user, isRestoring, login, logout }), [user, isRestoring])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
