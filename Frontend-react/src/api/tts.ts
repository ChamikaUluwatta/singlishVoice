const BASE_URL = import.meta.env.VITE_BACKEND_URL

export interface SpeechResult {
  audioUrl: string
  audioBlob: Blob
  transliteratedText: string
}

export async function healthCheck(): Promise<boolean> {
  try {
    const response = await fetch(`${BASE_URL}/health`)
    return response.ok
  } catch (error) {
    return false
  }
}

export async function generateSpeech(text: string, speaker: string): Promise<SpeechResult> {
  const res = await fetch(`${BASE_URL}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'audio/wav' },
    body: JSON.stringify({ text, speaker }),
  })
  if (!res.ok) throw new Error(`HTTP ${res.status}`)

  const disposition = res.headers.get('Content-Disposition') ?? ''
  let transliteratedText = 'Transliteration result'

  if (disposition.includes('filename*=')) {
    const encoded = disposition.split("''")[1]
    transliteratedText = decodeURIComponent(encoded)
  } else if (disposition.includes('filename=')) {
    transliteratedText = disposition.split('filename=')[1].replace(/"/g, '')
  }

  const audioBlob = await res.blob()
  const audioUrl = URL.createObjectURL(audioBlob)

  return { audioUrl, audioBlob, transliteratedText }
}
