import { useState } from 'react'
import { generateSpeech, type SpeechResult } from '../api/tts'
import { useBackendHealth } from '../hooks/useBackendHealth'

interface Props {
  onResults: (results: SpeechResult) => void
}

const SPEAKERS = [
  { label: 'Male (Mettananda)', value: 'mettananda' },
  { label: 'Female (Oshadi)', value: 'oshadi' },
] as const

type SpeakerValue = (typeof SPEAKERS)[number]['value']

export default function InputView({ onResults }: Props) {
  const backendStatus = useBackendHealth()
  const [text, setText] = useState<string>('')
  const [speaker, setSpeaker] = useState<SpeakerValue>('mettananda')
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)

  async function handleGenerate(): Promise<void> {
    if (!text.trim()) return
    setLoading(true)
    setError(null)
    try {
      const result = await generateSpeech(text, speaker)
      onResults(result)
    } catch (err) {
      setError('Failed to generate speech.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>SinglishVoice</h1>
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="e.g., oyata kohomada"
      />
      <select value={speaker} onChange={(e) => setSpeaker(e.target.value as SpeakerValue)}>
        {SPEAKERS.map((s) => (
          <option key={s.value} value={s.value}>
            {s.label}
          </option>
        ))}
      </select>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <button onClick={handleGenerate} disabled={loading || backendStatus !== 'ready'}>
        {loading ? 'Generating...' : 'Generate Speech'}
      </button>
    </div>
  )
}
