import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse 
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .models import TransliterationModel, TextToSpeechModel
from .dependencies import get_transliteration_model, get_tts_model, preload_models
from .utils import is_sinhala

app = FastAPI(
    title="SinglishVoice API",
    description="API for Romanized Sinhala TTS",
    version="1.0",
    on_startup=[preload_models]
)

origins = ["http://localhost", "http://localhost:8501"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to be converted to speech")
    speaker: str = Field(default="speaker_01", description="Speaker voice to use")

@app.post("/generate", tags=["TTS"])
async def generate_speech_endpoint(
    request_data: TTSRequest,
    nllb_model: TransliterationModel = Depends(get_transliteration_model),
    tts_model: TextToSpeechModel = Depends(get_tts_model)
):
    try:
        # 1. Transliteration
        if is_sinhala(request_data.text):
            sinhala_text_result = request_data.text
        else:
            sinhala_text_result = nllb_model.transliterate(request_data.text)

        # 2. TTS Synthesis
        final_text, saved_file_path = tts_model.synthesize(
            text=sinhala_text_result,
            speaker=request_data.speaker
        )

        # 3. Return audio file
        if saved_file_path and os.path.exists(saved_file_path):
            filename = os.path.basename(saved_file_path)
            return FileResponse(
                path=saved_file_path,
                media_type='audio/wav',
                filename=sinhala_text_result
            )
        else:
            raise HTTPException(status_code=404, detail="Generated audio file not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}