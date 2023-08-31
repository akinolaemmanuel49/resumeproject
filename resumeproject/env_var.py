from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    EMAIL_HOST: str
    EMAIL_HOST_USER: EmailStr
    EMAIL_HOST_PASSWORD: str
    EMAIL_PORT: int
    EMAIL_USE_TLS: bool
    DEFAULT_FROM_EMAIL: EmailStr

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
