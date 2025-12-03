from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path

load_dotenv()


class AppSettings(BaseSettings):
    BASE_DIR: Path = Path(__file__).parent.parent
    POSTGRES_USER: str = "test_user"
    POSTGRES_PASSWORD: str = "test_password"
    POSTGRES_HOST: str = "test_host"
    POSTGRES_DB_PORT: int = 5432
    POSTGRES_DB: str = "test_db"
    SOURCE_URL: str
    AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"

    class Config:
        env_file = "../../.env"
        env_prefix = ""


settings = AppSettings()
