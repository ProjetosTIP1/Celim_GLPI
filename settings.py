import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)
else:
    print(f".env file not found at {ENV_PATH}, proceeding without it.")


class Settings(BaseSettings):
    HORA_TERMINO: str = os.getenv("HORA_TERMINO", "06:50")
    CAMINHO_EXCEL: str = os.getenv(
        "CAMINHO_EXCEL",
        "C:\\Program Files\\Microsoft Office\\Office15\\EXCEL.EXE",
    )
    CHAVE: str = os.getenv("CHAVE", "")

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


try:
    settings = Settings()
except Exception as e:
    print(f"Error loading settings: {e}")
    raise
