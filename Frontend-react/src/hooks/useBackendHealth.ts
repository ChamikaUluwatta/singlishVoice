import { useEffect, useState } from 'react'
import { healthCheck } from '../api/tts'

export type BackendStatus = 'checking' | 'ready' | 'slow'

export function useBackendHealth(): BackendStatus {
  const [status, setStatus] = useState<BackendStatus>('checking')
  useEffect(() => {
    let attempt = 0
    let canceled = false

    async function poll(): Promise<void> {
      if (canceled) return
      const ready = await healthCheck()
      if (ready) {
        setStatus('ready')
      }

      attempt++
      if (attempt >= 6) {
        setStatus('slow')
      } else {
        setTimeout(poll, 1000)
      }
    }
    poll()

    return () => {
      canceled = true
    }
  }, [])

  return status
}
