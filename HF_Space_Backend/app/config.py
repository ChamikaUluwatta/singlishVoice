import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class Settings:
    HF_TOKEN: str = os.getenv("HF_TOKEN")
    NLLB_REPO: str = "Chamika1/NLLBSIRoman"
    VITS_REPO: str = "Chamika1/SinhalaVits"

settings = Settings()

if not settings.HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set in backend/.env file!")
