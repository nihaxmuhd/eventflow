import { Navigate, useLocation } from 'react-router-dom'
import { LoaderCircle } from 'lucide-react'
import { useAuth } from './auth'

export default function ProtectedRoute({ children }) {
  const { user, isRestoring } = useAuth()
  const location = useLocation()

  if (isRestoring) return <div className="grid min-h-screen place-items-center bg-[#f7f8fc]"><div className="flex items-center gap-3 text-sm font-medium text-slate-500"><LoaderCircle className="animate-spin text-indigo-600" size={20} /> Restoring your workspace...</div></div>
  return user ? children : <Navigate to="/login" replace state={{ from: location }} />
}
