import os
import io
import json
import torch
import time
import soundfile as sf
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from TTS.api import TTS as CoquiTTS
from huggingface_hub import snapshot_download
from .utils import normalize_numbers

class TransliterationModel:
    def __init__(self, model_repo: str, token: str):
        self.model_repo = model_repo
        self.token = token
        self.tokenizer = None
        self.model = None
        self._load_model()

    def _load_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_repo, token=self.token
        )
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_repo, token=self.token
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
    def __init__(self, model_repo: str, token: str):
        self.model_repo = model_repo
        self.token = token
        self.tts = None
        self._load_model()

    def _load_model(self):
        local_vits_dir = os.getenv("VITS_LOCAL_DIR", "/data/models/sinhala_vits")
        os.makedirs(local_vits_dir, exist_ok=True)

        vits_dir = snapshot_download(
            repo_id=self.model_repo,
            revision="main",
            token=self.token,
            local_dir=local_vits_dir,
            local_dir_use_symlinks=False
        )
        model_path = os.path.join(vits_dir, "best_model_31841.pth")
        config_path = os.path.join(vits_dir, "config.json")

        runtime_config_path = config_path
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        speakers_candidates = [
            os.path.join(vits_dir, "speaker.pth"),
            os.path.join(vits_dir, "speakers.pth"),
            os.path.join(vits_dir, "speaker", "speaker.pth"),
            os.path.join(vits_dir, "speaker", "speakers.pth"),
        ]
        resolved_speakers = next((p for p in speakers_candidates if os.path.exists(p)), None)
        if resolved_speakers:
            config_data["speakers_file"] = resolved_speakers
            model_args = config_data.get("model_args")
            if isinstance(model_args, dict):
                model_args["speakers_file"] = resolved_speakers
            runtime_config_path = os.path.join(vits_dir, "config.runtime.json")
            with open(runtime_config_path, "w", encoding="utf-8") as f:
                json.dump(config_data, f, ensure_ascii=True, indent=2)
        
        self.tts = CoquiTTS(
            model_path=model_path,
            config_path=runtime_config_path,
            progress_bar=False,
            gpu=torch.cuda.is_available()
        )

    def synthesize(self, text: str, speaker: str) -> tuple[str, bytes]:
        # Determine speaker parameters
        use_speaker_name = hasattr(self.tts, 'speakers') and self.tts.speakers and speaker in self.tts.speakers
        speaker_arg = speaker if use_speaker_name else None
        speaker_idx_arg = None
        
        if not use_speaker_name and hasattr(self.tts, 'speakers') and self.tts.speakers:
            speaker_arg = self.tts.speakers[0]
        
        # Generate audio
        wav = self.tts.tts(
            text=text,
            speaker=speaker_arg,
        )

        buffer = io.BytesIO()
        sf.write(buffer, wav, samplerate=self.tts.synthesizer.output_sample_rate, format="WAV")
        buffer.seek(0)

        return text, buffer.read()