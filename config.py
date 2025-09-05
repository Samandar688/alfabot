from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    BOT_TOKEN: str
    DB_URL: str
    BOT_ID: int
    ZAYAVKA_GROUP_ID: Optional[int] = None
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    ADMINS_ID: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
