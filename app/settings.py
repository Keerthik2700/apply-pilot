from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "ApplyPilot"
    ENV: str = "dev"
    SECRET_KEY: str
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()