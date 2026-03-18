import { useEffect, useState } from 'react'
import { healthCheck } from '../api/tts'

export type BackendStatus = 'ready' | 'starting'

export function useBackendHealth(): BackendStatus {
  const [status, setStatus] = useState<BackendStatus>('starting')
  
  useEffect(() => {
    let isMounted = true

    async function checkHealth() {
      try {
        const isHealthy = await healthCheck()
        if (isMounted) {
          setStatus(isHealthy ? 'ready' : 'starting')
        }
      } catch (error) {
        if (isMounted) {
          setStatus('starting')
        }
      }
    }

    checkHealth()
    const intervalId = setInterval(checkHealth, 30000)

    return () => {
      isMounted = false
      clearInterval(intervalId)
    }
  }, [])

  return status
}
