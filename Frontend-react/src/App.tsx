import { useState } from 'react'
import type { SpeechResult } from './api/tts'
import './App.css'
import ResultView from './components/ResultView'
import InputView from './components/InputView'

function App() {
  const [results, setResults] = useState<SpeechResult | null>(null)
  return results ? (
    <ResultView {...results} onReset={() => setResults(null)} />
  ) : (
    <InputView onResults={setResults} />
  )
}

export default App
