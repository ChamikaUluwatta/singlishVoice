import type { SpeechResult } from '../api/tts'

interface Props extends SpeechResult {
  onReset: () => void
}

export default function ResultView({ audioUrl, transliteratedText, onReset }: Props) {
  function handleDownload(): void {
    const a = document.createElement('a')
    a.href = audioUrl
    a.download = `${transliteratedText}.wav`
    a.click()
  }

  return (
    <div>
      <h1>Generated Output</h1>

      <h3>Transliteration Result</h3>
      <p>{transliteratedText}</p>

      <h3>Generated Audio</h3>
      <audio controls src={audioUrl} />

      <button onClick={handleDownload}>Download Audio</button>
      <button onClick={onReset}>Generate New</button>
    </div>
  )
}
