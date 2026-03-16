from functools import lru_cache
from .models import TransliterationModel, TextToSpeechModel
from .config import settings

startup_status = {
    "phase": "starting",
    "ready": False,
    "message": "Initializing backend",
    "error": None,
}


def _set_startup_status(phase: str, ready: bool, message: str, error: str | None = None):
    startup_status["phase"] = phase
    startup_status["ready"] = ready
    startup_status["message"] = message
    startup_status["error"] = error


def get_startup_status() -> dict:
    return dict(startup_status)

@lru_cache()
def get_transliteration_model() -> TransliterationModel:
    return TransliterationModel(
        model_repo=settings.NLLB_REPO,
        token=settings.HF_TOKEN
    )

@lru_cache()
def get_tts_model() -> TextToSpeechModel:
    return TextToSpeechModel(
        model_repo=settings.VITS_REPO,
        token=settings.HF_TOKEN
    )

def preload_models():
    try:
        _set_startup_status("loading_transliteration", False, "Loading transliteration model")
        get_transliteration_model()

        _set_startup_status("loading_tts", False, "Loading TTS model")
        get_tts_model()

        _set_startup_status("running", True, "Backend is ready")
    except Exception as exc:
        _set_startup_status("error", False, "Startup failed", str(exc))
        raise