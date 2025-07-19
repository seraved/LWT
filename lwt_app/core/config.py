import os

from pydantic_settings import BaseSettings


class EnvSettings(BaseSettings):
    DEBUG_MODE: bool = bool(os.getenv("DEBUG_MODE", True))


class Settings(EnvSettings):
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    BOT_ADMIN_USER_ID: int = int(os.getenv("BOT_ADMIN_USER_ID", 0))

    POSTGRES_HOST: str = str(os.getenv("POSTGRES_HOST", "127.0.0.1"))
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))
    POSTGRES_USER: str = str(os.getenv("POSTGRES_USER", "lwt_user"))
    POSTGRES_PASSWORD: str = str(os.getenv("DB_PASS", "lwt_password"))
    POSTGRES_DB: str = str(os.getenv("POSTGRES_DB", "lwt_db"))

    KINOPOISK_API_TOKEN: str = str(os.getenv("KINOPOISK_API_TOKEN", ""))
    KINOPOISK_RESULT_LIMIT: int = int(os.getenv("KINOPOISK_RESULT_LIMIT", 5))

    # Полный URL для базы данных (генерируется автоматически)

    @property
    def DB_DSN(self) -> str:
        # return f"postgresql+psycopg2://lwt_user:lwt_password@127.0.0.1:5432/lwt_db"
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def DB_DSN_async(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


# bot_settings = BotSettings()
settings = Settings()


__all__ = ['settings']
