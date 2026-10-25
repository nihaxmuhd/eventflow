import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import { AuthProvider, useAuth } from './auth.jsx'
import LoginPage from './LoginPage.jsx'
import ProtectedRoute from './ProtectedRoute.jsx'
import SchoolsPage from './SchoolsPage.jsx'
import StudentsPage from './StudentsPage.jsx'
import HousesPage from './HousesPage.jsx'

function AppRoutes() {
  const { user, logout } = useAuth()

  return <Routes>
    <Route path="/login" element={<LoginPage />} />
    <Route path="/" element={<ProtectedRoute><App user={user} onLogout={logout} /></ProtectedRoute>} />
    <Route path="/schools" element={<ProtectedRoute><SchoolsPage user={user} /></ProtectedRoute>} />
    <Route path="/students" element={<ProtectedRoute><StudentsPage user={user} /></ProtectedRoute>} />
    <Route path="/houses" element={<ProtectedRoute><HousesPage user={user} /></ProtectedRoute>} />
    <Route path="*" element={<ProtectedRoute><App user={user} onLogout={logout} /></ProtectedRoute>} />
  </Routes>
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  </StrictMode>,
)
