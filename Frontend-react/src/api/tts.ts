const RAW_BASE_URL = import.meta.env.VITE_BACKEND_URL

function getBaseUrl(): string {
  const baseUrl = RAW_BASE_URL?.trim()
  if (!baseUrl) {
    throw new Error('Missing VITE_BACKEND_URL. Set it in Frontend-react/.env and restart dev server.')
  }
  return baseUrl.replace(/\/+$/, '')
}

export interface SpeechResult {
  audioUrl: string
  audioBlob: Blob
  transliteratedText: string
}

export async function healthCheck(): Promise<boolean> {
  try {
    const response = await fetch(`${getBaseUrl()}/health`)
    return response.ok
  } catch (error) {
    return false
  }
}

export async function generateSpeech(text: string, speaker: string): Promise<SpeechResult> {
  const res = await fetch(`${getBaseUrl()}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, speaker }),
  })

  if (!res.ok) throw new Error(`HTTP ${res.status}`)

  const data = await res.json()

  const binaryString = atob(data.audio_base64)
  const bytes = Uint8Array.from(binaryString, (c) => c.charCodeAt(0))
  const audioBlob = new Blob([bytes], { type: 'audio/wav' })
  const audioUrl = URL.createObjectURL(audioBlob)

  return {
    audioUrl,
    audioBlob,
    transliteratedText: data.sinhala_text,
  }
}
