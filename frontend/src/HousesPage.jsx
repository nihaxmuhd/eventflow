import { useCallback, useEffect, useMemo, useState } from 'react'
import { ArrowLeft, ChevronLeft, ChevronRight, Edit3, Home, LoaderCircle, Plus, Search, Trash2, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import api from './api'
import { formatApiError } from './apiError'
import { useRealtimeEvents } from './useRealtimeEvents'

const PAGE_SIZE = 8
const emptyForm = { school: '', name: '', code: '', color: '#4F46E5', description: '', status: 'ACTIVE' }

const getError = (error, fallback) => {
  return formatApiError(error, fallback)
}

export default function HousesPage({ user }) {
  const navigate = useNavigate()
  const canManage = ['SUPER_ADMIN', 'ADMIN'].includes(user?.role)
  const isSuperAdmin = user?.role === 'SUPER_ADMIN'
  const [houses, setHouses] = useState([])
  const [schools, setSchools] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [query, setQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('ALL')
  const [page, setPage] = useState(1)
  const [formOpen, setFormOpen] = useState(false)
  const [editingHouse, setEditingHouse] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [formError, setFormError] = useState('')
  const [isSaving, setIsSaving] = useState(false)
  const [houseToDelete, setHouseToDelete] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)

  const loadData = useCallback(async () => {
    setIsLoading(true)
    setError('')
    try {
      const requests = [api.get('/houses/')]
      if (isSuperAdmin) requests.push(api.get('/schools/'))
      const [housesResponse, schoolsResponse] = await Promise.all(requests)
      setHouses(housesResponse.data)
      if (schoolsResponse) setSchools(schoolsResponse.data)
    } catch (requestError) {
      setError(getError(requestError, 'Unable to load houses. Please try again.'))
    } finally {
      setIsLoading(false)
    }
  }, [isSuperAdmin])

  useEffect(() => { loadData() }, [loadData])
  useRealtimeEvents(useCallback((event) => {
    if (event.type.startsWith('house.') || event.type.startsWith('student.') || event.type.startsWith('school.')) loadData().catch(() => {})
  }, [loadData]))
  useEffect(() => {
    if (!success) return undefined
    const timer = window.setTimeout(() => setSuccess(''), 3500)
    return () => window.clearTimeout(timer)
  }, [success])

  const schoolNames = useMemo(() => new Map(schools.map((school) => [school.id, school.name])), [schools])
  const filteredHouses = useMemo(() => {
    const search = query.trim().toLowerCase()
    return houses.filter((house) => (!search || [house.name, house.code, house.description].some((value) => value?.toLowerCase().includes(search))) && (statusFilter === 'ALL' || house.status === statusFilter))
  }, [houses, query, statusFilter])
  const totalPages = Math.max(1, Math.ceil(filteredHouses.length / PAGE_SIZE))
  const visibleHouses = filteredHouses.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  useEffect(() => { if (page > totalPages) setPage(totalPages) }, [page, totalPages])

  const openCreate = () => {
    setEditingHouse(null)
    setForm({ ...emptyForm })
    setFormError('')
    setFormOpen(true)
  }

  const openEdit = (house) => {
    setEditingHouse(house)
    setForm(Object.fromEntries(Object.keys(emptyForm).map((key) => [key, house[key] ?? ''])))
    setFormError('')
    setFormOpen(true)
  }

  const handleSave = async (event) => {
    event.preventDefault()
    setFormError('')
    setIsSaving(true)
    const payload = { ...form, school: isSuperAdmin ? Number(form.school) : undefined }
    if (!isSuperAdmin) delete payload.school
    try {
      if (editingHouse) {
        const response = await api.patch(`/houses/${editingHouse.id}/`, payload)
        setHouses((current) => current.map((house) => house.id === editingHouse.id ? response.data.data : house))
        setSuccess('House updated successfully.')
      } else {
        const response = await api.post('/houses/', payload)
        setHouses((current) => [response.data.data, ...current])
        setSuccess('House created successfully.')
      }
      setFormOpen(false)
    } catch (requestError) {
      setFormError(getError(requestError, 'Unable to save the house. Please try again.'))
    } finally {
      setIsSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!houseToDelete) return
    setIsDeleting(true)
    try {
      await api.delete(`/houses/${houseToDelete.id}/`)
      setHouses((current) => current.filter((house) => house.id !== houseToDelete.id))
      setHouseToDelete(null)
      setSuccess('House deleted successfully.')
    } catch (requestError) {
      setError(getError(requestError, 'Unable to delete the house. Please try again.'))
      setHouseToDelete(null)
    } finally {
      setIsDeleting(false)
    }
  }

  return <main className="min-h-screen bg-[#f7f8fc] p-4 sm:p-6 lg:p-8">
    <div className="mx-auto max-w-[1480px]">
      <header className="mb-7 flex flex-col justify-between gap-4 sm:flex-row sm:items-end"><div><button onClick={() => navigate('/')} className="inline-flex items-center gap-1.5 text-sm font-semibold text-indigo-600 hover:text-indigo-800"><ArrowLeft size={16} /> Dashboard</button><div className="mt-3 flex items-center gap-3"><span className="grid h-11 w-11 place-items-center rounded-xl bg-indigo-50 text-indigo-600"><Home size={21} /></span><div><h1 className="text-2xl font-bold tracking-tight text-slate-950 sm:text-3xl">Houses management</h1><p className="mt-1 text-sm text-slate-500">Organise houses, colours, and school groupings.</p></div></div></div>{canManage && <button onClick={openCreate} className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 transition hover:-translate-y-0.5 hover:bg-indigo-700"><Plus size={17} /> Add house</button>}</header>
      {success && <div role="status" className="mb-5 rounded-xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-700">{success}</div>}

      <section className="overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-sm shadow-slate-900/[0.02]"><div className="flex flex-col gap-4 border-b border-slate-100 p-5 sm:flex-row sm:items-center sm:justify-between sm:p-6"><div><h2 className="font-bold text-slate-900">All houses</h2><p className="mt-1 text-sm text-slate-500">{isLoading ? 'Loading houses...' : `${filteredHouses.length} house${filteredHouses.length === 1 ? '' : 's'} found`}</p></div><div className="flex w-full flex-col gap-3 sm:w-auto sm:flex-row"><label className="flex items-center gap-2 rounded-xl border border-slate-200 bg-slate-50/70 px-3 py-2.5 sm:w-72"><Search size={17} className="text-slate-400" /><input value={query} onChange={(event) => { setQuery(event.target.value); setPage(1) }} aria-label="Search houses" placeholder="Search houses..." className="w-full bg-transparent text-sm outline-none placeholder:text-slate-400" /></label><select value={statusFilter} onChange={(event) => { setStatusFilter(event.target.value); setPage(1) }} aria-label="Filter by status" className="rounded-xl border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-600 outline-none focus:border-indigo-400"><option value="ALL">All statuses</option><option value="ACTIVE">Active</option><option value="INACTIVE">Inactive</option></select></div></div>
        {error && <div role="alert" className="mx-5 mt-5 rounded-xl border border-rose-100 bg-rose-50 px-4 py-3 text-sm text-rose-700 sm:mx-6">{error}</div>}
        <div className="overflow-x-auto"><table className="w-full min-w-[820px] text-left text-sm"><thead><tr className="border-b border-slate-100 bg-slate-50/60 text-[11px] font-semibold uppercase tracking-wider text-slate-400"><th className="px-6 py-3.5">House</th><th className="px-4 py-3.5">Code</th>{isSuperAdmin && <th className="px-4 py-3.5">School</th>}<th className="px-4 py-3.5">Description</th><th className="px-4 py-3.5">Status</th>{canManage && <th className="w-24 px-4 py-3.5">Actions</th>}</tr></thead><tbody>{isLoading ? <tr><td colSpan={isSuperAdmin ? 6 : 5} className="px-6 py-12 text-center text-sm text-slate-500"><LoaderCircle className="mr-2 inline animate-spin text-indigo-600" size={18} /> Loading houses...</td></tr> : !error && visibleHouses.length === 0 ? <tr><td colSpan={isSuperAdmin ? 6 : 5} className="px-6 py-12 text-center text-sm text-slate-500">{query || statusFilter !== 'ALL' ? 'No houses match the current filters.' : 'No houses have been created yet.'}</td></tr> : visibleHouses.map((house) => <tr key={house.id} className="border-b border-slate-50 last:border-0 transition hover:bg-slate-50/70"><td className="px-6 py-4"><div className="flex items-center gap-3"><span className="h-9 w-2 rounded-full" style={{ backgroundColor: house.color }} /><div><p className="font-semibold text-slate-800">{house.name}</p><p className="mt-0.5 text-xs font-medium" style={{ color: house.color }}>{house.color}</p></div></div></td><td className="px-4 py-4 font-medium text-slate-600">{house.code}</td>{isSuperAdmin && <td className="px-4 py-4 text-slate-500">{schoolNames.get(house.school) || `School #${house.school}`}</td>}<td className="max-w-xs truncate px-4 py-4 text-slate-500">{house.description || '—'}</td><td className="px-4 py-4"><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${house.status === 'ACTIVE' ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'}`}>{house.status === 'ACTIVE' ? 'Active' : 'Inactive'}</span></td>{canManage && <td className="px-4 py-4"><div className="flex items-center gap-1"><button onClick={() => openEdit(house)} aria-label={`Edit ${house.name}`} className="rounded-lg p-2 text-slate-400 hover:bg-indigo-50 hover:text-indigo-600"><Edit3 size={16} /></button><button onClick={() => setHouseToDelete(house)} aria-label={`Delete ${house.name}`} className="rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-600"><Trash2 size={16} /></button></div></td>}</tr>)}</tbody></table></div>
        {!isLoading && filteredHouses.length > 0 && <div className="flex flex-col gap-3 border-t border-slate-100 px-5 py-4 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between sm:px-6"><p>Showing {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, filteredHouses.length)} of {filteredHouses.length}</p><div className="flex items-center gap-2"><button onClick={() => setPage((current) => Math.max(1, current - 1))} disabled={page === 1} className="rounded-lg border border-slate-200 p-2 disabled:cursor-not-allowed disabled:opacity-40"><ChevronLeft size={16} /></button><span className="min-w-20 text-center text-xs font-semibold text-slate-600">Page {page} of {totalPages}</span><button onClick={() => setPage((current) => Math.min(totalPages, current + 1))} disabled={page === totalPages} className="rounded-lg border border-slate-200 p-2 disabled:cursor-not-allowed disabled:opacity-40"><ChevronRight size={16} /></button></div></div>}
      </section>
    </div>

    {formOpen && <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-slate-950/40 p-4 py-8 backdrop-blur-sm"><section role="dialog" aria-modal="true" aria-labelledby="house-form-title" className="w-full max-w-2xl rounded-3xl bg-white shadow-2xl shadow-slate-950/20"><div className="flex items-center justify-between border-b border-slate-100 p-5 sm:p-6"><div><h2 id="house-form-title" className="text-lg font-bold text-slate-950">{editingHouse ? 'Edit house' : 'Add a house'}</h2><p className="mt-1 text-sm text-slate-500">House details are saved through the connected API.</p></div><button onClick={() => setFormOpen(false)} className="rounded-xl p-2 text-slate-400 hover:bg-slate-100"><X size={19} /></button></div><form onSubmit={handleSave} className="p-5 sm:p-6">{formError && <div role="alert" className="mb-5 rounded-xl border border-rose-100 bg-rose-50 px-4 py-3 text-sm text-rose-700">{formError}</div>}<div className="grid gap-4 sm:grid-cols-2">{isSuperAdmin && <label className="block sm:col-span-2"><span className="mb-1.5 block text-sm font-semibold text-slate-700">School</span><select required value={form.school} onChange={(event) => setForm({ ...form, school: event.target.value })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-50"><option value="">Select school</option>{schools.map((school) => <option key={school.id} value={school.id}>{school.name}</option>)}</select></label>}<label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">House name</span><input required value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-50" /></label><label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">House code</span><input required value={form.code} onChange={(event) => setForm({ ...form, code: event.target.value })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-50" /></label><label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">House colour</span><span className="flex h-11 items-center gap-3 rounded-xl border border-slate-200 bg-slate-50/60 px-3"><input required type="color" value={form.color} onChange={(event) => setForm({ ...form, color: event.target.value })} className="h-6 w-8 cursor-pointer border-0 bg-transparent p-0" /><input required pattern="^#[0-9A-Fa-f]{6}$" value={form.color} onChange={(event) => setForm({ ...form, color: event.target.value })} className="w-full bg-transparent text-sm outline-none" /></span></label><label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">Status</span><select value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none focus:border-indigo-400"><option value="ACTIVE">Active</option><option value="INACTIVE">Inactive</option></select></label><label className="block sm:col-span-2"><span className="mb-1.5 block text-sm font-semibold text-slate-700">Description</span><textarea value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} rows="4" className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50/60 px-3 py-2.5 text-sm outline-none focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-50" /></label></div><div className="mt-6 flex justify-end gap-3"><button type="button" onClick={() => setFormOpen(false)} className="rounded-xl px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100">Cancel</button><button disabled={isSaving} className="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-60">{isSaving && <LoaderCircle className="animate-spin" size={16} />}{isSaving ? 'Saving...' : editingHouse ? 'Save changes' : 'Create house'}</button></div></form></section></div>}
    {houseToDelete && <div className="fixed inset-0 z-[60] grid place-items-center bg-slate-950/45 p-4 backdrop-blur-sm"><section role="dialog" aria-modal="true" aria-labelledby="delete-house-title" className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl shadow-slate-950/20"><div className="grid h-11 w-11 place-items-center rounded-xl bg-rose-50 text-rose-600"><Trash2 size={20} /></div><h2 id="delete-house-title" className="mt-4 text-lg font-bold text-slate-950">Delete {houseToDelete.name}?</h2><p className="mt-2 text-sm leading-6 text-slate-500">This permanently deletes the house through the connected API and cannot be undone.</p><div className="mt-6 flex justify-end gap-3"><button disabled={isDeleting} onClick={() => setHouseToDelete(null)} className="rounded-xl px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100">Cancel</button><button disabled={isDeleting} onClick={handleDelete} className="inline-flex items-center gap-2 rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-rose-700 disabled:opacity-60">{isDeleting && <LoaderCircle className="animate-spin" size={16} />}{isDeleting ? 'Deleting...' : 'Delete house'}</button></div></section></div>}
  </main>
}
