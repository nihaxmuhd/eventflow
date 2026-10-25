export const EVENT_TYPES = new Set([
  'school.created', 'school.updated', 'school.deleted',
  'user.created',
  'student.created', 'student.updated', 'student.deleted',
  'house.created', 'house.updated', 'house.deleted',
  'event_category.created', 'event_category.updated', 'event_category.deleted',
  'event.created', 'event.updated', 'event.deleted',
  'registration.created', 'registration.updated', 'registration.deleted',
  'result.created', 'result.updated', 'result.deleted',
])

export function isRealtimeEvent(message) {
  const event = message?.event
  const data = event?.data
  if (message?.type !== 'event.update' || !EVENT_TYPES.has(event?.type) || !data || typeof data !== 'object') return false
  if (event.type.startsWith('school.')) return Number.isInteger(data.school_id)
  if (event.type === 'user.created') return Number.isInteger(data.user_id) && (data.school_id === null || Number.isInteger(data.school_id))
  if (event.type.startsWith('student.')) return Number.isInteger(data.student_id) && Number.isInteger(data.school_id)
  if (event.type.startsWith('house.')) return Number.isInteger(data.house_id) && Number.isInteger(data.school_id)
  if (event.type.startsWith('event_category.')) return Number.isInteger(data.event_category_id) && Number.isInteger(data.school_id)
  if (event.type.startsWith('event.')) return Number.isInteger(data.event_id) && Number.isInteger(data.school_id)
  if (event.type.startsWith('registration.')) return Number.isInteger(data.registration_id) && Number.isInteger(data.event_id) && typeof data.status === 'string'
  return Number.isInteger(data.result_id) && Number.isInteger(data.event_id) && Number.isInteger(data.registration_id) && Number.isInteger(data.position) && Number.isInteger(data.points)
}
