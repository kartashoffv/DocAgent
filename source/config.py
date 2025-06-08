import os
from dotenv import load_dotenv
from pydantic import BaseModel
from pathlib import Path
from openai import AsyncOpenAI

deployments_path = Path(__file__).parent.parent / "deployments" / ".env"
load_dotenv(dotenv_path=deployments_path)


class Config(BaseModel):
    PROJECT_DIR: str = str(Path(__file__).parent.parent)
    PROJECT_NAME: str = "DocAgent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "app")
    SQLALCHEMY_DATABASE_URI: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    )
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    IS_DEBUG: bool = os.getenv("IS_DEBUG", True)

    BACKEND_CORS_ORIGINS: list = os.getenv("BACKEND_CORS_ORIGINS", "*")
    
    API_BASE_URL: str = os.getenv("API_BASE_URL:{API_PORT}", f"http://localhost:{API_PORT}")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")


config = Config()
