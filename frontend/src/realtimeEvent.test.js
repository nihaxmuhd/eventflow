import test from 'node:test'
import assert from 'node:assert/strict'
import { isRealtimeEvent } from './realtimeEvent.js'

test('accepts minimal identifier-only payloads for every CRUD event family', () => {
  assert.equal(isRealtimeEvent({ type: 'event.update', event: { type: 'student.created', data: { student_id: 4, school_id: 2 } } }), true)
  assert.equal(isRealtimeEvent({ type: 'event.update', event: { type: 'house.deleted', data: { house_id: 7, school_id: 2 } } }), true)
  assert.equal(isRealtimeEvent({ type: 'event.update', event: { type: 'event.updated', data: { event_id: 9, school_id: 2 } } }), true)
  assert.equal(isRealtimeEvent({ type: 'event.update', event: { type: 'user.created', data: { user_id: 9, school_id: 2 } } }), true)
})

test('rejects malformed events before they reach page subscribers', () => {
  assert.equal(isRealtimeEvent({ type: 'event.update', event: { type: 'student.updated', data: { school_id: 2 } } }), false)
  assert.equal(isRealtimeEvent({ type: 'event.update', event: { type: 'unknown.created', data: { id: 1 } } }), false)
  assert.equal(isRealtimeEvent({ type: 'event.update', event: { type: 'result.created', data: { result_id: 1, event_id: 3, registration_id: 2, position: 1 } } }), false)
})
