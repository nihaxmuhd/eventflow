import { useCallback, useEffect, useState } from 'react'
import {
  ArrowUpRight, Bell, CalendarCheck, CalendarDays, CheckCircle2, ChevronDown,
  ClipboardList, Clock3, House, LayoutDashboard, LogOut, Menu, MoreHorizontal,
  Plus, Search, School, Settings, Sparkles, Trophy, Users, X,
} from 'lucide-react'
import api from './api'
import { useNavigate } from 'react-router-dom'
import './index.css'
import { useRealtimeEvents } from './useRealtimeEvents'

const navigation = [
  { label: 'Overview', icon: LayoutDashboard },
  { label: 'Schools', icon: School },
  { label: 'Students', icon: Users },
  { label: 'Houses', icon: House },
  { label: 'Categories', icon: ClipboardList },
  { label: 'Events', icon: CalendarDays },
  { label: 'Registrations', icon: CalendarCheck },
  { label: 'Results', icon: Trophy },
]

const iconTone = {
  blue: 'bg-blue-50 text-blue-600 ring-blue-100',
  violet: 'bg-violet-50 text-violet-600 ring-violet-100',
  amber: 'bg-amber-50 text-amber-600 ring-amber-100',
  emerald: 'bg-emerald-50 text-emerald-600 ring-emerald-100',
  rose: 'bg-rose-50 text-rose-600 ring-rose-100',
}

const eventTones = ['blue', 'violet', 'rose', 'amber']
const formatNumber = (value) => new Intl.NumberFormat().format(value || 0)
const formatDate = (value) => value ? new Intl.DateTimeFormat(undefined, { month: 'short', day: 'numeric', year: 'numeric' }).format(new Date(value)) : '—'
const readableStatus = (value) => value ? value.charAt(0) + value.slice(1).toLowerCase() : '—'

export default function App({ user, onLogout }) {
  const routerNavigate = useNavigate()
  const [active, setActive] = useState('Overview')
  const [menuOpen, setMenuOpen] = useState(false)
  const [isLoggingOut, setIsLoggingOut] = useState(false)
  const [overview, setOverview] = useState(null)
  const [overviewError, setOverviewError] = useState('')
  const [isOverviewLoading, setIsOverviewLoading] = useState(true)
  const [events, setEvents] = useState([])
  const [eventsError, setEventsError] = useState('')
  const [isEventsLoading, setIsEventsLoading] = useState(false)

  const displayName = [user?.first_name, user?.last_name].filter(Boolean).join(' ') || user?.username || 'Admin'
  const initials = displayName.split(' ').map((name) => name[0]).join('').slice(0, 2).toUpperCase()
  const role = user?.role?.replaceAll('_', ' ') || 'Administrator'
  const canManageWorkspace = ['SUPER_ADMIN', 'ADMIN'].includes(user?.role)
  const stats = [
    { label: 'Total students', value: overview?.total_students, icon: Users, tone: 'violet' },
    { label: 'Total events', value: overview?.total_events, icon: CalendarDays, tone: 'amber' },
    { label: 'Registrations', value: overview?.total_registrations, icon: ClipboardList, tone: 'emerald' },
    { label: 'Results recorded', value: overview?.total_results, icon: Trophy, tone: 'blue' },
  ]

  const navigate = (page) => {
    if (page === 'Schools' || page === 'Students' || page === 'Houses') {
      routerNavigate(page === 'Schools' ? '/schools' : page === 'Students' ? '/students' : '/houses')
      return
    }
    setActive(page)
    setMenuOpen(false)
  }
  const handleLogout = async () => { setIsLoggingOut(true); await onLogout() }

  const loadOverview = useCallback(async () => {
    setIsOverviewLoading(true)
    setOverviewError('')
    try {
      const response = await api.get('/dashboard/overview/')
      setOverview(response.data)
    } catch {
      setOverviewError('Unable to load dashboard totals.')
    } finally {
      setIsOverviewLoading(false)
    }
  }, [])

  useEffect(() => {
    loadOverview().catch(() => {})
  }, [loadOverview])

  useRealtimeEvents(useCallback((event) => {
    if (['student.', 'house.', 'event.', 'registration.', 'result.', 'school.'].some((prefix) => event.type.startsWith(prefix))) loadOverview().catch(() => {})
  }, [loadOverview]))

  const loadEvents = useCallback(async () => {
    if (!canManageWorkspace) return
    setIsEventsLoading(true)
    setEventsError('')
    try {
      const [eventsResponse, categoriesResponse] = await Promise.all([api.get('/events/'), api.get('/events/categories/')])
      const categoryNames = new Map(categoriesResponse.data.map((category) => [category.id, category.name]))
      setEvents(eventsResponse.data.map((event, index) => ({ ...event, categoryName: categoryNames.get(event.category) || `Category #${event.category}`, initials: event.name.split(' ').map((word) => word[0]).join('').slice(0, 2).toUpperCase(), tone: eventTones[index % eventTones.length] })))
    } catch { setEventsError('Unable to load events. Please try again.') } finally { setIsEventsLoading(false) }
  }, [canManageWorkspace])

  useEffect(() => { loadEvents().catch(() => {}) }, [loadEvents])
  useRealtimeEvents(useCallback((event) => {
    if (event.type.startsWith('event.') || event.type.startsWith('event_category.')) loadEvents().catch(() => {})
  }, [loadEvents]))

  return (
    <div className="min-h-screen bg-[#f7f8fc] text-slate-800 selection:bg-indigo-100">
      {menuOpen && <button aria-label="Close navigation" onClick={() => setMenuOpen(false)} className="fixed inset-0 z-40 bg-slate-950/35 backdrop-blur-[1px] lg:hidden" />}

      <aside className={`fixed inset-y-0 left-0 z-50 flex w-[272px] flex-col border-r border-slate-200/80 bg-white transition-transform duration-300 lg:translate-x-0 ${menuOpen ? 'translate-x-0 shadow-2xl shadow-slate-950/20' : '-translate-x-full'}`}>
        <div className="flex h-20 items-center justify-between border-b border-slate-100 px-5">
          <div className="flex items-center gap-3"><div className="grid h-10 w-10 place-items-center rounded-xl bg-gradient-to-br from-indigo-500 to-violet-700 text-sm font-black text-white shadow-lg shadow-indigo-500/25">E</div><div><p className="text-[15px] font-bold tracking-tight text-slate-950">EventFlow <span className="text-indigo-600">AI</span></p><p className="text-[11px] font-medium text-slate-400">Event management</p></div></div>
          <button onClick={() => setMenuOpen(false)} className="rounded-lg p-2 text-slate-400 hover:bg-slate-100 lg:hidden" aria-label="Close menu"><X size={18} /></button>
        </div>
        <div className="flex-1 overflow-y-auto px-4 py-6">
          <p className="mb-3 px-3 text-[10px] font-bold uppercase tracking-[0.18em] text-slate-400">Workspace</p>
          <nav className="space-y-1">{navigation.map(({ label, icon: Icon }) => <button key={label} onClick={() => navigate(label)} className={`group flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm font-medium transition-all ${active === label ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/20' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'}`}><Icon size={18} strokeWidth={active === label ? 2.25 : 1.9} /><span>{label}</span>{label === 'Events' && canManageWorkspace && <span className={`ml-auto rounded-md px-1.5 py-0.5 text-[10px] font-bold ${active === label ? 'bg-white/20 text-white' : 'bg-slate-100 text-slate-500'}`}>{overview?.total_events ?? '—'}</span>}</button>)}</nav>
        </div>
        <div className="border-t border-slate-100 p-4">
          <button onClick={() => navigate('Settings')} className={`mb-3 flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition ${active === 'Settings' ? 'bg-indigo-50 text-indigo-700' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-900'}`}><Settings size={18} /> Settings</button>
          <div className="rounded-xl bg-slate-50 p-2.5"><div className="flex items-center gap-3"><div className="grid h-9 w-9 place-items-center rounded-full bg-slate-900 text-xs font-bold text-white">{initials}</div><div className="min-w-0 flex-1"><p className="truncate text-sm font-semibold text-slate-800">{displayName}</p><p className="text-[11px] text-slate-500">{role}</p></div><ChevronDown size={16} className="text-slate-400" /></div><button onClick={handleLogout} disabled={isLoggingOut} className="mt-2 flex w-full items-center gap-2 rounded-lg px-2 py-1.5 text-xs font-semibold text-slate-500 transition hover:bg-white hover:text-rose-600 disabled:opacity-60"><LogOut size={14} /> {isLoggingOut ? 'Signing out...' : 'Sign out'}</button></div>
        </div>
      </aside>

      <div className="min-w-0 lg:pl-[272px]">
        <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-slate-200/75 bg-white/85 px-4 backdrop-blur-xl sm:px-8">
          <div className="flex items-center gap-3"><button onClick={() => setMenuOpen(true)} className="rounded-xl p-2 text-slate-600 hover:bg-slate-100 lg:hidden" aria-label="Open menu"><Menu size={21} /></button><div><p className="text-[11px] font-medium text-slate-400">Workspace <span className="px-1 text-slate-300">/</span> <span className="text-slate-500">{active}</span></p><h1 className="mt-0.5 text-lg font-bold tracking-tight text-slate-950">{active}</h1></div></div>
          <div className="flex items-center gap-2 sm:gap-3"><label className="hidden items-center gap-2 rounded-xl border border-slate-200 bg-slate-50/80 px-3 py-2 md:flex"><Search size={16} className="text-slate-400" /><input aria-label="Search" placeholder="Search anything..." className="w-40 bg-transparent text-sm outline-none placeholder:text-slate-400" /><kbd className="rounded border border-slate-200 bg-white px-1.5 py-0.5 text-[10px] font-medium text-slate-400">⌘ K</kbd></label><button aria-label="Search" className="rounded-xl border border-slate-200 p-2.5 text-slate-600 hover:bg-slate-50 md:hidden"><Search size={18} /></button><button aria-label="Notifications" className="relative rounded-xl border border-slate-200 p-2.5 text-slate-600 transition hover:bg-slate-50"><Bell size={18} /><span className="absolute right-2 top-2 h-2 w-2 rounded-full bg-rose-500 ring-2 ring-white" /></button><div className="grid h-9 w-9 place-items-center rounded-full bg-gradient-to-br from-slate-700 to-slate-950 text-xs font-bold text-white ring-2 ring-white">{initials}</div></div>
        </header>

        <main className="mx-auto max-w-[1680px] p-4 sm:p-6 lg:p-8">
          <div className="mb-7 flex flex-col justify-between gap-5 lg:flex-row lg:items-end"><div><div className="inline-flex items-center gap-1.5 rounded-full bg-indigo-50 px-3 py-1 text-xs font-semibold text-indigo-700"><Sparkles size={13} /> Your EventFlow workspace</div><h2 className="mt-3 text-2xl font-bold tracking-tight text-slate-950 sm:text-[30px]">Good morning, {displayName}</h2><p className="mt-2 text-sm text-slate-500">Here&apos;s a clear view of what&apos;s moving across your event workspace.</p></div>{canManageWorkspace && <button onClick={() => navigate('Events')} className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 transition hover:-translate-y-0.5 hover:bg-indigo-700"><Plus size={17} strokeWidth={2.5} /> Create event</button>}</div>

          <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 2xl:grid-cols-4">{stats.map(({ label, value, icon: Icon, tone }) => <article key={label} className="group rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm shadow-slate-900/[0.025] transition hover:-translate-y-0.5 hover:shadow-md"><div className="flex items-center justify-between"><p className="text-sm font-medium text-slate-500">{label}</p><span className={`grid h-10 w-10 place-items-center rounded-xl ring-1 ${iconTone[tone]}`}><Icon size={19} /></span></div><p className="mt-5 text-3xl font-bold tracking-tight text-slate-900">{isOverviewLoading ? <span className="inline-block h-8 w-16 animate-pulse rounded-lg bg-slate-100" /> : overviewError ? '—' : formatNumber(value)}</p><p className={`mt-2 flex items-center gap-1 text-xs font-medium ${overviewError ? 'text-rose-600' : 'text-emerald-600'}`}><ArrowUpRight size={14} /> {overviewError || 'Live workspace total'}</p></article>)}</section>

          <section className="mt-6 grid grid-cols-1 gap-6 2xl:grid-cols-[minmax(0,1fr)_360px]">
            <article className="overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-sm shadow-slate-900/[0.02]"><div className="flex flex-col gap-3 border-b border-slate-100 p-5 sm:flex-row sm:items-center sm:justify-between sm:p-6"><div><h3 className="font-bold tracking-tight text-slate-900">Events</h3><p className="mt-1 text-sm text-slate-500">Your current event collection.</p></div>{canManageWorkspace && <button onClick={() => navigate('Events')} className="text-left text-sm font-semibold text-indigo-600 hover:text-indigo-800">View all events →</button>}</div><div className="overflow-x-auto"><table className="w-full min-w-[660px] text-left text-sm"><thead><tr className="border-b border-slate-100 bg-slate-50/60 text-[11px] font-semibold uppercase tracking-wider text-slate-400"><th className="px-6 py-3.5">Event</th><th className="px-4 py-3.5">Category</th><th className="px-4 py-3.5">Created</th><th className="px-4 py-3.5">Status</th><th className="w-12 px-3 py-3.5" /></tr></thead><tbody>{!canManageWorkspace ? <tr><td colSpan="5" className="px-6 py-10 text-center text-sm text-slate-500">Event details are available to Super Admins and Admins.</td></tr> : isEventsLoading ? <tr><td colSpan="5" className="px-6 py-10 text-center text-sm text-slate-500">Loading events...</td></tr> : eventsError ? <tr><td colSpan="5" className="px-6 py-10 text-center text-sm text-rose-600">{eventsError}</td></tr> : events.length === 0 ? <tr><td colSpan="5" className="px-6 py-10 text-center text-sm text-slate-500">No events have been created yet.</td></tr> : events.map((event) => <tr key={event.id} className="border-b border-slate-50 last:border-0 transition hover:bg-slate-50/70"><td className="px-6 py-4"><div className="flex items-center gap-3"><span className={`grid h-9 w-9 place-items-center rounded-lg text-[10px] font-bold ${iconTone[event.tone]}`}>{event.initials}</span><span className="font-semibold text-slate-800">{event.name}</span></div></td><td className="px-4 py-4 text-slate-500">{event.categoryName}</td><td className="px-4 py-4"><p className="font-medium text-slate-700">{formatDate(event.created_at)}</p><p className="mt-0.5 text-xs text-slate-400">{event.code}</p></td><td className="px-4 py-4"><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${event.status === 'ACTIVE' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'}`}>{readableStatus(event.status)}</span></td><td className="px-3 py-4"><button aria-label={`More options for ${event.name}`} className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-600"><MoreHorizontal size={18} /></button></td></tr>)}</tbody></table></div></article>
            <div className="grid gap-6 sm:grid-cols-2 2xl:grid-cols-1"><article className="rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm shadow-slate-900/[0.02]"><h3 className="font-bold tracking-tight text-slate-900">Quick actions</h3><p className="mt-1 text-sm text-slate-500">Move work forward faster.</p><div className="mt-5 space-y-2.5">{(canManageWorkspace ? [['Add a student', Users, 'Students'], ['Manage schools', School, 'Schools'], ['Create a category', ClipboardList, 'Categories'], ['Enter results', Trophy, 'Results']] : [['View students', Users, 'Students'], ['View houses', House, 'Houses']]).map(([label, Icon, page]) => <button key={label} onClick={() => navigate(page)} className="group flex w-full items-center gap-3 rounded-xl border border-slate-100 p-2.5 text-left transition hover:border-indigo-100 hover:bg-indigo-50/50"><span className="grid h-9 w-9 place-items-center rounded-lg bg-slate-100 text-slate-600 transition group-hover:bg-white group-hover:text-indigo-600"><Icon size={17} /></span><span className="flex-1 text-sm font-medium text-slate-700">{label}</span><ArrowUpRight size={16} className="text-slate-300 transition group-hover:text-indigo-500" /></button>)}</div></article><article className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-indigo-600 via-indigo-600 to-violet-700 p-5 text-white shadow-lg shadow-indigo-600/20"><div className="absolute -right-7 -top-8 h-28 w-28 rounded-full bg-white/10" /><div className="relative"><span className="grid h-9 w-9 place-items-center rounded-xl bg-white/15"><Clock3 size={18} /></span><p className="mt-4 text-xs font-semibold uppercase tracking-wider text-indigo-200">Event collection</p><p className="mt-1 text-lg font-bold">{isOverviewLoading ? 'Loading...' : `${formatNumber(overview?.total_events)} total events`}</p><p className="mt-1 text-sm text-indigo-100">{overviewError || 'Live count from your workspace'}</p>{canManageWorkspace && <button onClick={() => navigate('Events')} className="mt-4 text-sm font-semibold text-white/90 hover:text-white">View event details →</button>}</div></article></div>
          </section>

          <section className="mt-6 grid grid-cols-1 gap-4 md:grid-cols-2"><article className="flex items-center gap-4 rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm shadow-slate-900/[0.02]"><span className="grid h-12 w-12 place-items-center rounded-xl bg-emerald-50 text-emerald-600"><CheckCircle2 size={22} /></span><div><p className="font-semibold text-slate-900">Top house</p><p className="mt-1 text-sm text-slate-500">{isOverviewLoading ? 'Loading workspace data...' : overview?.top_house ? `${overview.top_house} · ${formatNumber(overview.top_house_points)} points` : 'No house results recorded yet.'}</p></div></article><article className="flex items-center gap-4 rounded-2xl border border-slate-200/80 bg-white p-5 shadow-sm shadow-slate-900/[0.02]"><span className="grid h-12 w-12 place-items-center rounded-xl bg-violet-50 text-violet-600"><Trophy size={22} /></span><div><p className="font-semibold text-slate-900">Top student</p><p className="mt-1 text-sm text-slate-500">{isOverviewLoading ? 'Loading workspace data...' : overview?.top_student ? `${overview.top_student} · ${formatNumber(overview.top_student_points)} points` : 'No student results recorded yet.'}</p></div><button onClick={() => navigate('Results')} className="ml-auto rounded-lg p-2 text-slate-400 hover:bg-slate-50 hover:text-indigo-600"><ArrowUpRight size={19} /></button></article></section>
          <footer className="py-8 text-center text-xs font-medium text-slate-400">EventFlow AI · School Event Management System</footer>
        </main>
      </div>
    </div>
  )
}
