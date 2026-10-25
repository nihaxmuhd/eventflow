import test from 'node:test'
import assert from 'node:assert/strict'
import { parseApiError } from './apiError.js'

const responseError = (status, data) => ({ response: { status, data } })

test('parses DRF field and duplicate validation errors', () => {
  const duplicate = parseApiError(responseError(400, { email: ['A student with this email address already exists.'] }))
  assert.equal(duplicate.fieldErrors.email, 'This email address is already registered.')
  const required = parseApiError(responseError(400, { admission_number: ['This field is required.'] }))
  assert.equal(required.fieldErrors.admission_number, 'This field is required.')
})

test('handles invalid foreign keys, non-field errors, and HTTP status errors', () => {
  assert.equal(parseApiError(responseError(400, { house: ['Invalid pk "2" - object does not exist.'] })).fieldErrors.house, 'Please select a valid house.')
  assert.equal(parseApiError(responseError(400, { non_field_errors: ['This student is already registered.'] })).message, 'This student is already registered.')
  assert.equal(parseApiError(responseError(401, {})).message, 'Your session has expired. Please sign in again.')
  assert.equal(parseApiError(responseError(403, {})).message, 'You do not have permission to perform this action.')
  assert.equal(parseApiError(responseError(404, {})).message, 'The requested record could not be found.')
  assert.equal(parseApiError(responseError(500, '<html>error</html>')).message, 'The server is temporarily unavailable. Please try again.')
})

test('handles network and non-JSON failures without displaying response bodies', () => {
  assert.equal(parseApiError({ request: {} }).message, 'The server is temporarily unavailable. Please try again.')
  assert.equal(parseApiError(responseError(400, '<html>bad gateway</html>')).fieldErrors.email, undefined)
})
