import { useCallback, useEffect, useMemo, useState } from 'react'
import { ArrowLeft, ChevronLeft, ChevronRight, Edit3, LoaderCircle, Plus, Search, School, Trash2, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import api from './api'
import { formatApiError } from './apiError'
import { useRealtimeEvents } from './useRealtimeEvents'

const PAGE_SIZE = 8
const emptyForm = {
  name: '', code: '', email: '', phone: '', website: '', address: '',
  city: '', state: '', country: 'India', pincode: '', status: 'ACTIVE',
}

const getError = (error, fallback) => {
  return formatApiError(error, fallback)
}

export default function SchoolsPage({ user }) {
  const navigate = useNavigate()
  const isSuperAdmin = user?.role === 'SUPER_ADMIN'
  const [schools, setSchools] = useState([])
  const [isLoading, setIsLoading] = useState(isSuperAdmin)
  const [error, setError] = useState('')
  const [query, setQuery] = useState('')
  const [page, setPage] = useState(1)
  const [formOpen, setFormOpen] = useState(false)
  const [editingSchool, setEditingSchool] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [formError, setFormError] = useState('')
  const [isSaving, setIsSaving] = useState(false)
  const [schoolToDelete, setSchoolToDelete] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)

  const loadSchools = useCallback(async () => {
    setIsLoading(true)
    setError('')
    try {
      const response = await api.get('/schools/')
      setSchools(response.data)
    } catch (requestError) {
      setError(getError(requestError, 'Unable to load schools. Please try again.'))
    } finally {
      setIsLoading(false)
    }
  }, [])

  useEffect(() => {
    if (isSuperAdmin) loadSchools()
  }, [isSuperAdmin, loadSchools])
  useRealtimeEvents(useCallback((event) => {
    if (event.type.startsWith('school.')) loadSchools().catch(() => {})
  }, [loadSchools]))

  const filteredSchools = useMemo(() => {
    const search = query.trim().toLowerCase()
    if (!search) return schools
    return schools.filter((school) => [school.name, school.code, school.city, school.email].some((value) => value?.toLowerCase().includes(search)))
  }, [schools, query])
  const totalPages = Math.max(1, Math.ceil(filteredSchools.length / PAGE_SIZE))
  const visibleSchools = filteredSchools.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  useEffect(() => { if (page > totalPages) setPage(totalPages) }, [page, totalPages])

  const openCreate = () => {
    setEditingSchool(null)
    setForm(emptyForm)
    setFormError('')
    setFormOpen(true)
  }

  const openEdit = (school) => {
    setEditingSchool(school)
    setForm(Object.fromEntries(Object.keys(emptyForm).map((key) => [key, school[key] || (key === 'country' ? 'India' : '')])))
    setFormError('')
    setFormOpen(true)
  }

  const handleSave = async (event) => {
    event.preventDefault()
    setIsSaving(true)
    setFormError('')
    try {
      if (editingSchool) {
        const response = await api.patch(`/schools/${editingSchool.id}/`, form)
        setSchools((current) => current.map((school) => school.id === editingSchool.id ? response.data : school))
      } else {
        const response = await api.post('/schools/', form)
        setSchools((current) => [response.data, ...current])
      }
      setFormOpen(false)
    } catch (requestError) {
      setFormError(getError(requestError, 'Unable to save the school. Please try again.'))
    } finally {
      setIsSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!schoolToDelete) return
    setIsDeleting(true)
    try {
      await api.delete(`/schools/${schoolToDelete.id}/`)
      setSchools((current) => current.filter((school) => school.id !== schoolToDelete.id))
      setSchoolToDelete(null)
    } catch (requestError) {
      setError(getError(requestError, 'Unable to delete the school. Please try again.'))
      setSchoolToDelete(null)
    } finally {
      setIsDeleting(false)
    }
  }

  if (!isSuperAdmin) {
    return <main className="grid min-h-screen place-items-center bg-[#f7f8fc] p-5"><section className="w-full max-w-md rounded-3xl border border-slate-200 bg-white p-8 text-center shadow-xl shadow-slate-900/[0.05]"><div className="mx-auto grid h-12 w-12 place-items-center rounded-xl bg-rose-50 text-rose-600"><School size={23} /></div><h1 className="mt-5 text-xl font-bold text-slate-950">Schools access is restricted</h1><p className="mt-2 text-sm leading-6 text-slate-500">The connected backend allows school management only for Super Admins.</p><button onClick={() => navigate('/')} className="mt-6 inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700"><ArrowLeft size={16} /> Back to dashboard</button></section></main>
  }

  return <main className="min-h-screen bg-[#f7f8fc] p-4 sm:p-6 lg:p-8">
    <div className="mx-auto max-w-[1480px]">
      <header className="mb-7 flex flex-col justify-between gap-4 sm:flex-row sm:items-end"><div><button onClick={() => navigate('/')} className="inline-flex items-center gap-1.5 text-sm font-semibold text-indigo-600 hover:text-indigo-800"><ArrowLeft size={16} /> Dashboard</button><div className="mt-3 flex items-center gap-3"><span className="grid h-11 w-11 place-items-center rounded-xl bg-indigo-50 text-indigo-600"><School size={21} /></span><div><h1 className="text-2xl font-bold tracking-tight text-slate-950 sm:text-3xl">Schools management</h1><p className="mt-1 text-sm text-slate-500">Create and maintain schools in your EventFlow workspace.</p></div></div></div><button onClick={openCreate} className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 transition hover:-translate-y-0.5 hover:bg-indigo-700"><Plus size={17} /> Add school</button></header>

      <section className="overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-sm shadow-slate-900/[0.02]">
        <div className="flex flex-col gap-4 border-b border-slate-100 p-5 sm:flex-row sm:items-center sm:justify-between sm:p-6"><div><h2 className="font-bold text-slate-900">All schools</h2><p className="mt-1 text-sm text-slate-500">{isLoading ? 'Loading schools...' : `${filteredSchools.length} school${filteredSchools.length === 1 ? '' : 's'} found`}</p></div><label className="flex w-full items-center gap-2 rounded-xl border border-slate-200 bg-slate-50/70 px-3 py-2.5 sm:w-72"><Search size={17} className="text-slate-400" /><input value={query} onChange={(event) => { setQuery(event.target.value); setPage(1) }} aria-label="Search schools" placeholder="Search schools..." className="w-full bg-transparent text-sm outline-none placeholder:text-slate-400" /></label></div>
        {error && <div role="alert" className="mx-5 mt-5 rounded-xl border border-rose-100 bg-rose-50 px-4 py-3 text-sm text-rose-700 sm:mx-6">{error}</div>}
        <div className="overflow-x-auto"><table className="w-full min-w-[850px] text-left text-sm"><thead><tr className="border-b border-slate-100 bg-slate-50/60 text-[11px] font-semibold uppercase tracking-wider text-slate-400"><th className="px-6 py-3.5">School</th><th className="px-4 py-3.5">Code</th><th className="px-4 py-3.5">Location</th><th className="px-4 py-3.5">Contact</th><th className="px-4 py-3.5">Status</th><th className="w-24 px-4 py-3.5">Actions</th></tr></thead><tbody>{isLoading ? <tr><td colSpan="6" className="px-6 py-12 text-center text-sm text-slate-500"><LoaderCircle className="mr-2 inline animate-spin text-indigo-600" size={18} /> Loading schools...</td></tr> : !error && visibleSchools.length === 0 ? <tr><td colSpan="6" className="px-6 py-12 text-center text-sm text-slate-500">{query ? 'No schools match your search.' : 'No schools have been created yet.'}</td></tr> : visibleSchools.map((school) => <tr key={school.id} className="border-b border-slate-50 last:border-0 transition hover:bg-slate-50/70"><td className="px-6 py-4"><div className="flex items-center gap-3"><span className="grid h-9 w-9 place-items-center rounded-lg bg-indigo-50 text-xs font-bold text-indigo-600">{school.name.slice(0, 2).toUpperCase()}</span><div><p className="font-semibold text-slate-800">{school.name}</p><p className="mt-0.5 text-xs text-slate-400">{school.email || 'No email added'}</p></div></div></td><td className="px-4 py-4 font-medium text-slate-600">{school.code}</td><td className="px-4 py-4 text-slate-500">{[school.city, school.state].filter(Boolean).join(', ') || '—'}</td><td className="px-4 py-4 text-slate-500">{school.phone || '—'}</td><td className="px-4 py-4"><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${school.status === 'ACTIVE' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'}`}>{school.status === 'ACTIVE' ? 'Active' : 'Inactive'}</span></td><td className="px-4 py-4"><div className="flex items-center gap-1"><button onClick={() => openEdit(school)} aria-label={`Edit ${school.name}`} className="rounded-lg p-2 text-slate-400 hover:bg-indigo-50 hover:text-indigo-600"><Edit3 size={16} /></button><button onClick={() => setSchoolToDelete(school)} aria-label={`Delete ${school.name}`} className="rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-600"><Trash2 size={16} /></button></div></td></tr>)}</tbody></table></div>
        {!isLoading && filteredSchools.length > 0 && <div className="flex flex-col gap-3 border-t border-slate-100 px-5 py-4 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between sm:px-6"><p>Showing {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, filteredSchools.length)} of {filteredSchools.length}</p><div className="flex items-center gap-2"><button onClick={() => setPage((current) => Math.max(1, current - 1))} disabled={page === 1} className="rounded-lg border border-slate-200 p-2 disabled:cursor-not-allowed disabled:opacity-40"><ChevronLeft size={16} /></button><span className="min-w-20 text-center text-xs font-semibold text-slate-600">Page {page} of {totalPages}</span><button onClick={() => setPage((current) => Math.min(totalPages, current + 1))} disabled={page === totalPages} className="rounded-lg border border-slate-200 p-2 disabled:cursor-not-allowed disabled:opacity-40"><ChevronRight size={16} /></button></div></div>}
      </section>
    </div>

    {formOpen && <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-slate-950/40 p-4 py-8 backdrop-blur-sm"><section role="dialog" aria-modal="true" aria-labelledby="school-form-title" className="w-full max-w-2xl rounded-3xl bg-white shadow-2xl shadow-slate-950/20"><div className="flex items-center justify-between border-b border-slate-100 p-5 sm:p-6"><div><h2 id="school-form-title" className="text-lg font-bold text-slate-950">{editingSchool ? 'Edit school' : 'Add a school'}</h2><p className="mt-1 text-sm text-slate-500">All fields use the connected school API.</p></div><button onClick={() => setFormOpen(false)} className="rounded-xl p-2 text-slate-400 hover:bg-slate-100"><X size={19} /></button></div><form onSubmit={handleSave} className="p-5 sm:p-6">{formError && <div role="alert" className="mb-5 rounded-xl border border-rose-100 bg-rose-50 px-4 py-3 text-sm text-rose-700">{formError}</div>}<div className="grid gap-4 sm:grid-cols-2">{[['name', 'School name', true], ['code', 'School code', true], ['email', 'Email'], ['phone', 'Phone'], ['website', 'Website'], ['city', 'City'], ['state', 'State'], ['country', 'Country'], ['pincode', 'Pincode']].map(([field, label, required]) => <label key={field} className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">{label}</span><input required={required} type={field === 'email' ? 'email' : field === 'website' ? 'url' : 'text'} value={form[field]} onChange={(event) => setForm({ ...form, [field]: event.target.value })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-50" /></label>)}<label className="block sm:col-span-2"><span className="mb-1.5 block text-sm font-semibold text-slate-700">Address</span><textarea value={form.address} onChange={(event) => setForm({ ...form, address: event.target.value })} rows="3" className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50/60 px-3 py-2.5 text-sm outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-50" /></label><label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">Status</span><select value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-50"><option value="ACTIVE">Active</option><option value="INACTIVE">Inactive</option></select></label></div><div className="mt-6 flex justify-end gap-3"><button type="button" onClick={() => setFormOpen(false)} className="rounded-xl px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100">Cancel</button><button disabled={isSaving} className="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-60">{isSaving && <LoaderCircle className="animate-spin" size={16} />}{isSaving ? 'Saving...' : editingSchool ? 'Save changes' : 'Create school'}</button></div></form></section></div>}
    {schoolToDelete && <div className="fixed inset-0 z-[60] grid place-items-center bg-slate-950/45 p-4 backdrop-blur-sm"><section role="dialog" aria-modal="true" aria-labelledby="delete-school-title" className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl shadow-slate-950/20"><div className="grid h-11 w-11 place-items-center rounded-xl bg-rose-50 text-rose-600"><Trash2 size={20} /></div><h2 id="delete-school-title" className="mt-4 text-lg font-bold text-slate-950">Delete {schoolToDelete.name}?</h2><p className="mt-2 text-sm leading-6 text-slate-500">This permanently deletes the school through the connected API and cannot be undone.</p><div className="mt-6 flex justify-end gap-3"><button disabled={isDeleting} onClick={() => setSchoolToDelete(null)} className="rounded-xl px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100">Cancel</button><button disabled={isDeleting} onClick={handleDelete} className="inline-flex items-center gap-2 rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-rose-700 disabled:opacity-60">{isDeleting && <LoaderCircle className="animate-spin" size={16} />}{isDeleting ? 'Deleting...' : 'Delete school'}</button></div></section></div>}
  </main>
}
