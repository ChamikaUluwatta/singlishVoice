import os
import base64
import logging
import traceback
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
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

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("singlishvoice.api")

# Set to 1 only while debugging. Keep 0 in production.
DEBUG_ERRORS = os.getenv("DEBUG_ERRORS", "0") == "1"


def _get_allowed_origins() -> list[str]:
    raw = os.getenv("CORS_ALLOW_ORIGINS", "https://singlish-voice.vercel.app")
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins or ["https://singlish-voice.vercel.app"]


allowed_origins = _get_allowed_origins()
allow_all_origins = "*" in allowed_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all_origins else allowed_origins,
    # Browsers reject credentialed CORS responses when origin is '*'.
    allow_credentials=not allow_all_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TTSRequest(BaseModel):
    text: str = Field(..., description="Text to be converted to speech")
    speaker: str = Field(default="speaker_01", description="Speaker voice to use")


@app.exception_handler(Exception)
async def unhandled_exception_handler(request, exc):
    trace = traceback.format_exc()
    logger.error("Unhandled exception on %s %s\n%s", request.method, request.url.path, trace)
    detail = {
        "error": str(exc),
        "type": exc.__class__.__name__,
    }
    if DEBUG_ERRORS:
        detail["traceback"] = trace
    return JSONResponse(status_code=500, content={"detail": detail})

@app.post("/generate", tags=["TTS"])
async def generate_speech_endpoint(
    request_data: TTSRequest,
    nllb_model: TransliterationModel = Depends(get_transliteration_model),
    tts_model: TextToSpeechModel = Depends(get_tts_model)
):
    try:
        sinhala_text = (
            request_data.text 
            if is_sinhala(request_data.text) 
            else nllb_model.transliterate(request_data.text)
        )

        _, audio_bytes = tts_model.synthesize(
            text=sinhala_text,
            speaker=request_data.speaker
        )

        audio_base64 = base64.b64encode(audio_bytes).decode("utf-8")

        return {
            "sinhala_text": sinhala_text,
            "audio_base64": audio_base64
        }

    except Exception as e:
        trace = traceback.format_exc()
        logger.error("generate_speech failed\n%s", trace)
        detail = {
            "error": str(e),
            "type": e.__class__.__name__,
        }
        if DEBUG_ERRORS:
            detail["traceback"] = trace
        raise HTTPException(status_code=500, detail=detail)

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}