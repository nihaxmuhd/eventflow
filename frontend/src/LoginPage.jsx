import { useState } from 'react'
import { ArrowRight, Eye, EyeOff, KeyRound, LoaderCircle, LockKeyhole, ShieldCheck, Sparkles, UserRound } from 'lucide-react'
import { Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from './auth'
import { parseApiError } from './apiError'

export default function LoginPage() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [credentials, setCredentials] = useState({ login: '', password: '' })
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  if (user) return <Navigate to="/" replace />

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setIsSubmitting(true)
    try {
      await login(credentials.login, credentials.password)
      navigate('/', { replace: true })
    } catch (requestError) {
      setError(parseApiError(requestError, 'Invalid username/email or password.').message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return <main className="relative grid min-h-screen overflow-hidden bg-[#f7f8fc] lg:grid-cols-[1.1fr_0.9fr]">
    <section className="relative hidden overflow-hidden bg-gradient-to-br from-slate-950 via-indigo-950 to-violet-900 p-12 text-white lg:flex lg:flex-col xl:p-16">
      <div className="absolute -left-24 top-24 h-72 w-72 rounded-full bg-indigo-400/20 blur-3xl" /><div className="absolute -bottom-20 right-0 h-80 w-80 rounded-full bg-violet-400/20 blur-3xl" />
      <div className="relative flex items-center gap-3"><div className="grid h-11 w-11 place-items-center rounded-xl bg-white text-sm font-black text-indigo-700 shadow-lg shadow-indigo-950/30">E</div><div><p className="font-bold tracking-tight">EventFlow AI</p><p className="text-xs text-indigo-200">Event management</p></div></div>
      <div className="relative my-auto max-w-lg"><div className="mb-6 inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/10 px-3 py-1.5 text-xs font-semibold text-indigo-100"><Sparkles size={14} /> Built for exceptional events</div><h1 className="text-4xl font-bold leading-tight tracking-tight xl:text-5xl">Bring every school event into perfect flow.</h1><p className="mt-5 max-w-md text-base leading-7 text-indigo-100/80">Plan, coordinate, and celebrate every achievement from one beautifully organised workspace.</p><div className="mt-10 grid grid-cols-3 gap-3"><div className="rounded-2xl border border-white/10 bg-white/[0.07] p-4"><p className="text-2xl font-bold">24</p><p className="mt-1 text-xs text-indigo-200">Active events</p></div><div className="rounded-2xl border border-white/10 bg-white/[0.07] p-4"><p className="text-2xl font-bold">2.4k</p><p className="mt-1 text-xs text-indigo-200">Students</p></div><div className="rounded-2xl border border-white/10 bg-white/[0.07] p-4"><p className="text-2xl font-bold">12</p><p className="mt-1 text-xs text-indigo-200">Schools</p></div></div></div>
      <p className="relative text-xs text-indigo-200/70">Secure access for your EventFlow workspace.</p>
    </section>
    <section className="relative flex items-center justify-center p-5 sm:p-8"><div className="absolute -right-24 top-0 h-72 w-72 rounded-full bg-indigo-100/70 blur-3xl lg:hidden" /><div className="relative w-full max-w-[420px]"><div className="mb-10 flex items-center gap-3 lg:hidden"><div className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-indigo-500 to-violet-700 text-sm font-black text-white shadow-lg shadow-indigo-500/25">E</div><div><p className="font-bold tracking-tight text-slate-950">EventFlow <span className="text-indigo-600">AI</span></p><p className="text-xs text-slate-400">Event management</p></div></div><div className="rounded-3xl border border-slate-200/80 bg-white p-6 shadow-xl shadow-slate-900/[0.06] sm:p-8"><div className="grid h-11 w-11 place-items-center rounded-xl bg-indigo-50 text-indigo-600"><LockKeyhole size={21} /></div><h2 className="mt-5 text-2xl font-bold tracking-tight text-slate-950">Welcome back</h2><p className="mt-2 text-sm leading-6 text-slate-500">Sign in to manage your events, teams, and results.</p>{error && <div role="alert" className="mt-5 rounded-xl border border-rose-100 bg-rose-50 px-3.5 py-3 text-sm text-rose-700">{error}</div>}<form className="mt-6 space-y-4" onSubmit={handleSubmit}><label className="block"><span className="mb-2 block text-sm font-semibold text-slate-700">Username or email</span><span className="flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50/50 px-3 transition focus-within:border-indigo-400 focus-within:bg-white focus-within:ring-4 focus-within:ring-indigo-50"><UserRound size={17} className="text-slate-400" /><input required autoComplete="username" value={credentials.login} onChange={(event) => setCredentials({ ...credentials, login: event.target.value })} placeholder="Enter your username or email" className="h-11 w-full bg-transparent text-sm outline-none placeholder:text-slate-400" /></span></label><label className="block"><span className="mb-2 block text-sm font-semibold text-slate-700">Password</span><span className="flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50/50 px-3 transition focus-within:border-indigo-400 focus-within:bg-white focus-within:ring-4 focus-within:ring-indigo-50"><KeyRound size={17} className="text-slate-400" /><input required autoComplete="current-password" type={showPassword ? 'text' : 'password'} value={credentials.password} onChange={(event) => setCredentials({ ...credentials, password: event.target.value })} placeholder="Enter your password" className="h-11 w-full bg-transparent text-sm outline-none placeholder:text-slate-400" /><button type="button" aria-label={showPassword ? 'Hide password' : 'Show password'} onClick={() => setShowPassword(!showPassword)} className="rounded-md p-1 text-slate-400 hover:text-slate-600">{showPassword ? <EyeOff size={18} /> : <Eye size={18} />}</button></span></label><button disabled={isSubmitting} className="mt-2 flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-indigo-600 text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 transition hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-70">{isSubmitting ? <><LoaderCircle className="animate-spin" size={18} /> Signing in...</> : <>Sign in <ArrowRight size={17} /></>}</button></form><div className="mt-6 flex items-center justify-center gap-2 text-xs text-slate-400"><ShieldCheck size={15} className="text-emerald-500" /> Your session is protected with secure authentication.</div></div></div></section>
  </main>
}
