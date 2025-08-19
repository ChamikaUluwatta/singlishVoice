import os
import torch
import time
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from TTS.api import TTS as CoquiTTS
from huggingface_hub import snapshot_download
from .utils import normalize_numbers

class TransliterationModel:
    def __init__(self, model_repo: str, auth_token: str):
        self.model_repo = model_repo
        self.auth_token = auth_token
        self.tokenizer = None
        self.model = None
        self._load_model()

    def _load_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_repo, use_auth_token=self.auth_token
        )
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_repo, use_auth_token=self.auth_token
        )
        if torch.cuda.is_available():
            self.model.to("cuda")

    def transliterate(self, text: str) -> str:
        text = normalize_numbers(text)
        inputs = self.tokenizer(text, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}
        
        outputs = self.model.generate(**inputs, max_length=100)
        translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translated_text

class TextToSpeechModel:
    def __init__(self, model_repo: str, auth_token: str):
        self.model_repo = model_repo
        self.auth_token = auth_token
        self.tts = None
        self._load_model()

    def _load_model(self):
        vits_dir = snapshot_download(
            repo_id=self.model_repo,
            revision="main",
            use_auth_token=self.auth_token,
            local_dir_use_symlinks=False
        )
        model_path = os.path.join(vits_dir, "best_model_31841.pth")
        config_path = os.path.join(vits_dir, "config.json")
        
        self.tts = CoquiTTS(
            model_path=model_path,
            config_path=config_path,
            progress_bar=False,
            gpu=torch.cuda.is_available()
        )

    def synthesize(self, text: str, speaker: str) -> tuple[str, str]:
        audio_save_directory = "/content/FYP/GeneratedWaves"
        
        # Generate unique filename
        timestamp = int(time.time())
        output_filename = f"audio_{timestamp}_{speaker}.wav"
        output_path = os.path.join(audio_save_directory, output_filename)
        
        # Determine speaker parameters
        use_speaker_name = hasattr(self.tts, 'speakers') and self.tts.speakers and speaker in self.tts.speakers
        speaker_arg = speaker if use_speaker_name else None
        speaker_idx_arg = None
        
        if not use_speaker_name and hasattr(self.tts, 'speakers') and self.tts.speakers:
            speaker_arg = self.tts.speakers[0]
        
        # Generate audio
        self.tts.tts_to_file(
            text=text,
            speaker=speaker_arg,
            speaker_idx=speaker_idx_arg,
            file_path=output_path
        )

        return text, output_path