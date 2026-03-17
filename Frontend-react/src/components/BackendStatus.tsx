import type { BackendStatus } from '../hooks/useBackendHealth'

interface Props {
  status: BackendStatus
}

export default function BackendStatus({ status }: Props) {
  if (status === 'checking') return <p>Checking Backend ...</p>
  if (status === 'ready') return <p>Backend is ready</p>
  if (status === 'slow') return <p>Backend is slow</p>
  return <p>Backend is still starting up...</p>
}
