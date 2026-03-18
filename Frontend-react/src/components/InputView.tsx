import { useState } from 'react'
import { generateSpeech, type SpeechResult } from '../api/tts'
import { useBackendHealth } from '../hooks/useBackendHealth'
import '@material/web/button/filled-button.js'
import '@material/web/button/outlined-button.js'
import '@material/web/textfield/filled-text-field.js'
import '@material/web/select/filled-select.js'
import '@material/web/select/select-option.js'

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
    <div className="input-view">
      <div className="wrapper">
        <svg>
          <text x="50%" y="50%" dy=".35em" textAnchor="middle">
            SinglishVoice
          </text>
        </svg>
      </div>

      <section className="backend-panel" aria-live="polite">
        <p className="backend-status-row">
          Backend status:
          <span
            className={`status-pill ${backendStatus === 'ready' ? 'status-ready' : 'status-not-ready'}`}
          >
            {backendStatus === 'ready' ? 'Ready' : 'Not Ready'}
          </span>
          <md-outlined-button
            className="start-backend-btn"
            onClick={() =>
              window.open(
                'https://huggingface.co/spaces/Chamika1/SinglishVoiceBackend',
                '_blank',
                'noopener,noreferrer'
              )
            }
          >
            Start the Backend
          </md-outlined-button>
        </p>
      </section>

      <div className="input-group">
        <md-filled-text-field
          label="Text"
          value={text}
          onInput={(e) => setText((e.target as HTMLInputElement).value)}
          placeholder="e.g., oyata kohomada"
        ></md-filled-text-field>

        <md-filled-select
          label="Speaker"
          value={speaker}
          onChange={(e) => setSpeaker((e.target as HTMLSelectElement).value as SpeakerValue)}
        >
          {SPEAKERS.map((s) => (
            <md-select-option key={s.value} value={s.value} selected={speaker === s.value}>
              <div slot="headline">{s.label}</div>
            </md-select-option>
          ))}
        </md-filled-select>
      </div>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      <md-filled-button
        className="generate-btn"
        onClick={handleGenerate}
        disabled={loading || backendStatus !== 'ready'}
      >
        {loading ? 'Generating...' : 'Generate Speech'}
      </md-filled-button>
    </div>
  )
}
