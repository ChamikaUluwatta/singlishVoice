from functools import lru_cache
from .models import TransliterationModel, TextToSpeechModel
from .config import settings

@lru_cache()
def get_transliteration_model() -> TransliterationModel:
    return TransliterationModel(
        model_repo=settings.NLLB_REPO,
        auth_token=settings.HF_TOKEN
    )

@lru_cache()
def get_tts_model() -> TextToSpeechModel:
    return TextToSpeechModel(
        model_repo=settings.VITS_REPO,
        auth_token=settings.HF_TOKEN
    )

def preload_models():
    get_transliteration_model()
    get_tts_model()