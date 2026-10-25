const GENERIC_SERVER_ERROR = 'The server is temporarily unavailable. Please try again.'

function firstMessage(value) {
  if (Array.isArray(value)) return firstMessage(value[0])
  return typeof value === 'string' ? value : ''
}

function userMessage(field, message) {
  const normalized = message.toLowerCase()
  if (field === 'email' && /(already|exists|used|unique)/.test(normalized)) return 'This email address is already registered.'
  if (field === 'admission_number' && /(already|exists|unique)/.test(normalized)) return 'This admission number already exists.'
  if ((field === 'house' || field === 'school') && /(exist|valid|incorrect)/.test(normalized)) return `Please select a valid ${field}.`
  return message
}

export function parseApiError(error, fallback = 'Please correct the highlighted fields.') {
  const response = error?.response
  if (!response) return { message: 'The server is temporarily unavailable. Please try again.', fieldErrors: {} }

  const { status, data } = response
  if (status === 401) return { message: 'Your session has expired. Please sign in again.', fieldErrors: {} }
  if (status === 403) return { message: 'You do not have permission to perform this action.', fieldErrors: {} }
  if (status === 404) return { message: 'The requested record could not be found.', fieldErrors: {} }
  if (status >= 500) return { message: GENERIC_SERVER_ERROR, fieldErrors: {} }
  if (!data || typeof data !== 'object' || Array.isArray(data)) return { message: fallback, fieldErrors: {} }

  const fieldErrors = {}
  let message = firstMessage(data.detail) || firstMessage(data.message) || firstMessage(data.non_field_errors)
  for (const [field, value] of Object.entries(data)) {
    if (['detail', 'message', 'non_field_errors', 'success', 'data'].includes(field)) continue
    const fieldMessage = firstMessage(value)
    if (fieldMessage) fieldErrors[field] = userMessage(field, fieldMessage)
  }
  if (!message && Object.keys(fieldErrors).length) message = 'Please correct the highlighted fields.'
  return { message: message || fallback, fieldErrors }
}

export function formatApiError(error, fallback) {
  const parsed = parseApiError(error, fallback)
  const fields = Object.entries(parsed.fieldErrors).map(([field, message]) => `${field.replace(/_/g, ' ')}: ${message}`)
  return [...new Set([parsed.message, ...fields])].join(' ')
}
