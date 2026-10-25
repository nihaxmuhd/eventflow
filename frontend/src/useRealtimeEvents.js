import { useEffect } from 'react'
import { realtimeClient } from './realtime'

export function useRealtimeEvents(handler) {
  useEffect(() => realtimeClient.subscribe(handler), [handler])
}
