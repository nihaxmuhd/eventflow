import { useCallback, useEffect, useMemo, useState } from 'react'
import { ArrowLeft, ChevronLeft, ChevronRight, Edit3, LoaderCircle, Plus, Search, Trash2, Users, X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import api from './api'
import { formatApiError, parseApiError } from './apiError'
import { useRealtimeEvents } from './useRealtimeEvents'

const PAGE_SIZE = 8
const emptyForm = {
  school: '', house: '', admission_number: '', first_name: '', last_name: '',
  gender: 'MALE', date_of_birth: '', class_name: '', division: '', parent_name: '',
  parent_phone: '', student_phone: '', email: '', address: '', status: 'ACTIVE',
}

const displayStatus = (status) => status.charAt(0) + status.slice(1).toLowerCase()

export default function StudentsPage({ user }) {
  const navigate = useNavigate()
  const canManage = ['SUPER_ADMIN', 'ADMIN'].includes(user?.role)
  const isSuperAdmin = user?.role === 'SUPER_ADMIN'
  const [students, setStudents] = useState([])
  const [houses, setHouses] = useState([])
  const [schools, setSchools] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')
  const [query, setQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState('ALL')
  const [genderFilter, setGenderFilter] = useState('ALL')
  const [classFilter, setClassFilter] = useState('ALL')
  const [page, setPage] = useState(1)
  const [formOpen, setFormOpen] = useState(false)
  const [editingStudent, setEditingStudent] = useState(null)
  const [form, setForm] = useState(emptyForm)
  const [formError, setFormError] = useState('')
  const [isSaving, setIsSaving] = useState(false)
  const [studentToDelete, setStudentToDelete] = useState(null)
  const [isDeleting, setIsDeleting] = useState(false)
  const [success, setSuccess] = useState('')

  const loadData = useCallback(async () => {
    setIsLoading(true)
    setError('')
    try {
      const requests = [api.get('/students/'), api.get('/houses/')]
      if (isSuperAdmin) requests.push(api.get('/schools/'))
      const [studentsResponse, housesResponse, schoolsResponse] = await Promise.all(requests)
      setStudents(studentsResponse.data)
      setHouses(housesResponse.data)
      if (schoolsResponse) setSchools(schoolsResponse.data)
    } catch (requestError) {
      setError(parseApiError(requestError, 'Unable to load student data. Please try again.').message)
    } finally {
      setIsLoading(false)
    }
  }, [isSuperAdmin])

  useEffect(() => { loadData() }, [loadData])
  useRealtimeEvents(useCallback((event) => {
    if (event.type.startsWith('student.') || event.type.startsWith('house.') || event.type.startsWith('school.')) loadData().catch(() => {})
  }, [loadData]))
  useEffect(() => {
    if (!success) return undefined
    const timer = window.setTimeout(() => setSuccess(''), 3500)
    return () => window.clearTimeout(timer)
  }, [success])

  const schoolNames = useMemo(() => new Map(schools.map((school) => [school.id, school.name])), [schools])
  const houseNames = useMemo(() => new Map(houses.map((house) => [house.id, house.name])), [houses])
  const classOptions = useMemo(() => [...new Set(students.map((student) => student.class_name).filter(Boolean))].sort(), [students])
  const filteredStudents = useMemo(() => {
    const search = query.trim().toLowerCase()
    return students.filter((student) => {
      const matchesSearch = !search || [student.full_name, student.admission_number, student.email, student.parent_phone].some((value) => value?.toLowerCase().includes(search))
      return matchesSearch
        && (statusFilter === 'ALL' || student.status === statusFilter)
        && (genderFilter === 'ALL' || student.gender === genderFilter)
        && (classFilter === 'ALL' || student.class_name === classFilter)
    })
  }, [students, query, statusFilter, genderFilter, classFilter])
  const totalPages = Math.max(1, Math.ceil(filteredStudents.length / PAGE_SIZE))
  const visibleStudents = filteredStudents.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE)

  useEffect(() => { if (page > totalPages) setPage(totalPages) }, [page, totalPages])

  const setFilter = (setter, value) => { setter(value); setPage(1) }
  const allowedHouses = form.school ? houses.filter((house) => String(house.school) === String(form.school)) : houses

  const openCreate = () => {
    setEditingStudent(null)
    setForm({ ...emptyForm })
    setFormError('')
    setFormOpen(true)
  }

  const openEdit = (student) => {
    setEditingStudent(student)
    setForm(Object.fromEntries(Object.keys(emptyForm).map((key) => [key, student[key] ?? ''])))
    setFormError('')
    setFormOpen(true)
  }

  const handleSave = async (event) => {
    event.preventDefault()
    setFormError('')
    setIsSaving(true)
    const payload = {
      ...form,
      school: isSuperAdmin ? Number(form.school) : undefined,
      house: form.house ? Number(form.house) : null,
      date_of_birth: form.date_of_birth || null,
    }
    if (!isSuperAdmin) delete payload.school
    try {
      if (editingStudent) {
        const response = await api.patch(`/students/${editingStudent.id}/`, payload)
        setStudents((current) => current.map((student) => student.id === editingStudent.id ? response.data.data : student))
        setSuccess('Student updated successfully.')
      } else {
        const response = await api.post('/students/', payload)
        setStudents((current) => [response.data.data, ...current])
        setSuccess('Student created successfully.')
      }
      setFormOpen(false)
    } catch (requestError) {
      setFormError(formatApiError(requestError, 'Unable to save the student. Please try again.'))
    } finally {
      setIsSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!studentToDelete) return
    setIsDeleting(true)
    try {
      await api.delete(`/students/${studentToDelete.id}/`)
      setStudents((current) => current.filter((student) => student.id !== studentToDelete.id))
      setStudentToDelete(null)
      setSuccess('Student deleted successfully.')
    } catch (requestError) {
      setError(parseApiError(requestError, 'Unable to delete the student. Please try again.').message)
      setStudentToDelete(null)
    } finally {
      setIsDeleting(false)
    }
  }


  return <main className="min-h-screen bg-[#f7f8fc] p-4 sm:p-6 lg:p-8">
    <div className="mx-auto max-w-[1580px]">
      <header className="mb-7 flex flex-col justify-between gap-4 sm:flex-row sm:items-end"><div><button onClick={() => navigate('/')} className="inline-flex items-center gap-1.5 text-sm font-semibold text-indigo-600 hover:text-indigo-800"><ArrowLeft size={16} /> Dashboard</button><div className="mt-3 flex items-center gap-3"><span className="grid h-11 w-11 place-items-center rounded-xl bg-indigo-50 text-indigo-600"><Users size={21} /></span><div><h1 className="text-2xl font-bold tracking-tight text-slate-950 sm:text-3xl">Students management</h1><p className="mt-1 text-sm text-slate-500">Search, organise, and maintain your school&apos;s students.</p></div></div></div>{canManage && <button onClick={openCreate} className="inline-flex items-center justify-center gap-2 rounded-xl bg-indigo-600 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/20 transition hover:-translate-y-0.5 hover:bg-indigo-700"><Plus size={17} /> Add student</button>}</header>
      {success && <div role="status" className="mb-5 rounded-xl border border-emerald-100 bg-emerald-50 px-4 py-3 text-sm font-medium text-emerald-700">{success}</div>}

      <section className="overflow-hidden rounded-2xl border border-slate-200/80 bg-white shadow-sm shadow-slate-900/[0.02]">
        <div className="border-b border-slate-100 p-5 sm:p-6"><div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between"><div><h2 className="font-bold text-slate-900">All students</h2><p className="mt-1 text-sm text-slate-500">{isLoading ? 'Loading students...' : `${filteredStudents.length} student${filteredStudents.length === 1 ? '' : 's'} found`}</p></div><label className="flex w-full items-center gap-2 rounded-xl border border-slate-200 bg-slate-50/70 px-3 py-2.5 xl:w-80"><Search size={17} className="text-slate-400" /><input value={query} onChange={(event) => setFilter(setQuery, event.target.value)} aria-label="Search students" placeholder="Search name, admission no..." className="w-full bg-transparent text-sm outline-none placeholder:text-slate-400" /></label></div><div className="mt-4 grid gap-3 sm:grid-cols-3"><select value={statusFilter} onChange={(event) => setFilter(setStatusFilter, event.target.value)} aria-label="Filter by status" className="h-10 rounded-xl border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-600 outline-none focus:border-indigo-400"><option value="ALL">All statuses</option><option value="ACTIVE">Active</option><option value="INACTIVE">Inactive</option><option value="ALUMNI">Alumni</option></select><select value={genderFilter} onChange={(event) => setFilter(setGenderFilter, event.target.value)} aria-label="Filter by gender" className="h-10 rounded-xl border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-600 outline-none focus:border-indigo-400"><option value="ALL">All genders</option><option value="MALE">Male</option><option value="FEMALE">Female</option><option value="OTHER">Other</option></select><select value={classFilter} onChange={(event) => setFilter(setClassFilter, event.target.value)} aria-label="Filter by class" className="h-10 rounded-xl border border-slate-200 bg-slate-50/70 px-3 text-sm text-slate-600 outline-none focus:border-indigo-400"><option value="ALL">All classes</option>{classOptions.map((className) => <option key={className} value={className}>{className}</option>)}</select></div></div>
        {error && <div role="alert" className="mx-5 mt-5 rounded-xl border border-rose-100 bg-rose-50 px-4 py-3 text-sm text-rose-700 sm:mx-6">{error}</div>}
        <div className="overflow-x-auto"><table className="w-full min-w-[980px] text-left text-sm"><thead><tr className="border-b border-slate-100 bg-slate-50/60 text-[11px] font-semibold uppercase tracking-wider text-slate-400"><th className="px-6 py-3.5">Student</th><th className="px-4 py-3.5">Admission no.</th><th className="px-4 py-3.5">Class</th><th className="px-4 py-3.5">House</th>{isSuperAdmin && <th className="px-4 py-3.5">School</th>}<th className="px-4 py-3.5">Status</th>{canManage && <th className="w-24 px-4 py-3.5">Actions</th>}</tr></thead><tbody>{isLoading ? <tr><td colSpan={isSuperAdmin ? 7 : 6} className="px-6 py-12 text-center text-sm text-slate-500"><LoaderCircle className="mr-2 inline animate-spin text-indigo-600" size={18} /> Loading students...</td></tr> : !error && visibleStudents.length === 0 ? <tr><td colSpan={isSuperAdmin ? 7 : 6} className="px-6 py-12 text-center text-sm text-slate-500">{query || statusFilter !== 'ALL' || genderFilter !== 'ALL' || classFilter !== 'ALL' ? 'No students match the current filters.' : 'No students have been created yet.'}</td></tr> : visibleStudents.map((student) => <tr key={student.id} className="border-b border-slate-50 last:border-0 transition hover:bg-slate-50/70"><td className="px-6 py-4"><div className="flex items-center gap-3"><span className="grid h-9 w-9 place-items-center rounded-full bg-indigo-50 text-xs font-bold text-indigo-600">{student.full_name.split(' ').map((name) => name[0]).join('').slice(0, 2).toUpperCase()}</span><div><p className="font-semibold text-slate-800">{student.full_name}</p><p className="mt-0.5 text-xs text-slate-400">{student.email || student.parent_phone || 'No contact added'}</p></div></div></td><td className="px-4 py-4 font-medium text-slate-600">{student.admission_number}</td><td className="px-4 py-4 text-slate-500">{student.class_name} {student.division}</td><td className="px-4 py-4 text-slate-500">{houseNames.get(student.house) || '—'}</td>{isSuperAdmin && <td className="px-4 py-4 text-slate-500">{schoolNames.get(student.school) || `School #${student.school}`}</td>}<td className="px-4 py-4"><span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${student.status === 'ACTIVE' ? 'bg-emerald-50 text-emerald-700' : student.status === 'ALUMNI' ? 'bg-violet-50 text-violet-700' : 'bg-slate-100 text-slate-600'}`}>{displayStatus(student.status)}</span></td>{canManage && <td className="px-4 py-4"><div className="flex items-center gap-1"><button onClick={() => openEdit(student)} aria-label={`Edit ${student.full_name}`} className="rounded-lg p-2 text-slate-400 hover:bg-indigo-50 hover:text-indigo-600"><Edit3 size={16} /></button><button onClick={() => setStudentToDelete(student)} aria-label={`Delete ${student.full_name}`} className="rounded-lg p-2 text-slate-400 hover:bg-rose-50 hover:text-rose-600"><Trash2 size={16} /></button></div></td>}</tr>)}</tbody></table></div>
        {!isLoading && filteredStudents.length > 0 && <div className="flex flex-col gap-3 border-t border-slate-100 px-5 py-4 text-sm text-slate-500 sm:flex-row sm:items-center sm:justify-between sm:px-6"><p>Showing {(page - 1) * PAGE_SIZE + 1}–{Math.min(page * PAGE_SIZE, filteredStudents.length)} of {filteredStudents.length}</p><div className="flex items-center gap-2"><button onClick={() => setPage((current) => Math.max(1, current - 1))} disabled={page === 1} className="rounded-lg border border-slate-200 p-2 disabled:cursor-not-allowed disabled:opacity-40"><ChevronLeft size={16} /></button><span className="min-w-20 text-center text-xs font-semibold text-slate-600">Page {page} of {totalPages}</span><button onClick={() => setPage((current) => Math.min(totalPages, current + 1))} disabled={page === totalPages} className="rounded-lg border border-slate-200 p-2 disabled:cursor-not-allowed disabled:opacity-40"><ChevronRight size={16} /></button></div></div>}
      </section>
    </div>

    {formOpen && <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-slate-950/40 p-4 py-8 backdrop-blur-sm"><section role="dialog" aria-modal="true" aria-labelledby="student-form-title" className="w-full max-w-3xl rounded-3xl bg-white shadow-2xl shadow-slate-950/20"><div className="flex items-center justify-between border-b border-slate-100 p-5 sm:p-6"><div><h2 id="student-form-title" className="text-lg font-bold text-slate-950">{editingStudent ? 'Edit student' : 'Add a student'}</h2><p className="mt-1 text-sm text-slate-500">Student details are saved through the connected API.</p></div><button onClick={() => setFormOpen(false)} className="rounded-xl p-2 text-slate-400 hover:bg-slate-100"><X size={19} /></button></div><form onSubmit={handleSave} className="p-5 sm:p-6">{formError && <div role="alert" className="mb-5 rounded-xl border border-rose-100 bg-rose-50 px-4 py-3 text-sm text-rose-700">{formError}</div>}<div className="grid gap-4 sm:grid-cols-2">{isSuperAdmin && <label className="block sm:col-span-2"><span className="mb-1.5 block text-sm font-semibold text-slate-700">School</span><select required value={form.school} onChange={(event) => setForm({ ...form, school: event.target.value, house: '' })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-50"><option value="">Select school</option>{schools.map((school) => <option key={school.id} value={school.id}>{school.name}</option>)}</select></label>}{[['admission_number', 'Admission number', true], ['first_name', 'First name', true], ['last_name', 'Last name'], ['class_name', 'Class', true], ['division', 'Division', true], ['parent_name', 'Parent name'], ['parent_phone', 'Parent phone'], ['student_phone', 'Student phone'], ['email', 'Email']].map(([field, label, required]) => <label key={field} className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">{label}</span><input required={required} type={field === 'email' ? 'email' : 'text'} value={form[field]} onChange={(event) => setForm({ ...form, [field]: event.target.value })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none transition focus:border-indigo-400 focus:bg-white focus:ring-4 focus:ring-indigo-50" /></label>)}<label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">Gender</span><select value={form.gender} onChange={(event) => setForm({ ...form, gender: event.target.value })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none focus:border-indigo-400"><option value="MALE">Male</option><option value="FEMALE">Female</option><option value="OTHER">Other</option></select></label><label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">Date of birth</span><input type="date" value={form.date_of_birth} onChange={(event) => setForm({ ...form, date_of_birth: event.target.value })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none focus:border-indigo-400" /></label><label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">House</span><select value={form.house} onChange={(event) => setForm({ ...form, house: event.target.value })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none focus:border-indigo-400"><option value="">No house</option>{allowedHouses.map((house) => <option key={house.id} value={house.id}>{house.name}</option>)}</select></label><label className="block"><span className="mb-1.5 block text-sm font-semibold text-slate-700">Status</span><select value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value })} className="h-11 w-full rounded-xl border border-slate-200 bg-slate-50/60 px-3 text-sm outline-none focus:border-indigo-400"><option value="ACTIVE">Active</option><option value="INACTIVE">Inactive</option><option value="ALUMNI">Alumni</option></select></label><label className="block sm:col-span-2"><span className="mb-1.5 block text-sm font-semibold text-slate-700">Address</span><textarea value={form.address} onChange={(event) => setForm({ ...form, address: event.target.value })} rows="3" className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50/60 px-3 py-2.5 text-sm outline-none focus:border-indigo-400" /></label></div><div className="mt-6 flex justify-end gap-3"><button type="button" onClick={() => setFormOpen(false)} className="rounded-xl px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100">Cancel</button><button disabled={isSaving} className="inline-flex items-center gap-2 rounded-xl bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-60">{isSaving && <LoaderCircle className="animate-spin" size={16} />}{isSaving ? 'Saving...' : editingStudent ? 'Save changes' : 'Create student'}</button></div></form></section></div>}
    {studentToDelete && <div className="fixed inset-0 z-[60] grid place-items-center bg-slate-950/45 p-4 backdrop-blur-sm"><section role="dialog" aria-modal="true" aria-labelledby="delete-student-title" className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl shadow-slate-950/20"><div className="grid h-11 w-11 place-items-center rounded-xl bg-rose-50 text-rose-600"><Trash2 size={20} /></div><h2 id="delete-student-title" className="mt-4 text-lg font-bold text-slate-950">Delete {studentToDelete.full_name}?</h2><p className="mt-2 text-sm leading-6 text-slate-500">This permanently deletes the student through the connected API. It may be blocked when related records exist.</p><div className="mt-6 flex justify-end gap-3"><button disabled={isDeleting} onClick={() => setStudentToDelete(null)} className="rounded-xl px-4 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-100">Cancel</button><button disabled={isDeleting} onClick={handleDelete} className="inline-flex items-center gap-2 rounded-xl bg-rose-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-rose-700 disabled:opacity-60">{isDeleting && <LoaderCircle className="animate-spin" size={16} />}{isDeleting ? 'Deleting...' : 'Delete student'}</button></div></section></div>}
  </main>
}
