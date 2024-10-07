from pydantic_settings import BaseSettings, SettingsConfigDict
import pathlib

BASE_DIR = pathlib.Path(__file__).parent


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore"
    )


Config = Settings()
