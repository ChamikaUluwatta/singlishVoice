import type { BackendStatus } from '../hooks/useBackendHealth'

interface Props {
    status: BackendStatus
}

export default function BackendStatus({ status }: Props) {
    if (status === 'ready') return <p>Backend is ready</p>
    return <p>Backend is still starting up...</p>
}