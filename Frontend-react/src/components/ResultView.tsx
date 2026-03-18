import type { SpeechResult } from '../api/tts'
import '@material/web/button/filled-button.js'
import '@material/web/button/outlined-button.js'

interface Props extends SpeechResult {
  onReset: () => void
}

export default function ResultView({ audioUrl, transliteratedText, onReset }: Props) {
  function handleDownload(): void {
    const a = document.createElement('a')
    a.href = audioUrl
    a.download = `audio.wav`
    a.click()
  }

  return (
    <div className="result-view">
      <h1>Generated Output</h1>

      <h3>Transliteration Result</h3>
      <p>{transliteratedText}</p>

      <h3>Generated Audio</h3>
      <audio controls src={audioUrl} />

      <div className="result-actions">
        <md-filled-button onClick={handleDownload}>Download Audio</md-filled-button>
        <md-outlined-button onClick={onReset}>Generate New</md-outlined-button>
      </div>
    </div>
  )
}
