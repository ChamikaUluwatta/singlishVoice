import { useState } from 'react'
import type { SpeechResult } from './api/tts'
import './App.css'
import ResultView from './components/ResultView'
import InputView from './components/InputView'

function App() {
  const [results, setResults] = useState<SpeechResult | null>(null)
  return <main className='app-shell'>
    {results ? (
      <ResultView {...results} onReset={() => setResults(null)} />
    ) : (
      <InputView onResults={setResults} />
    )}
  </main>
}

export default App
