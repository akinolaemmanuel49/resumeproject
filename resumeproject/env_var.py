from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = "/etc/secrets/.env" if os.path.exists("/etc/secrets/.env") else ".env"


class Settings(BaseSettings):
    SECRET_KEY: str
    BASE_URL: str
    MAILGUN_API_KEY: str
    MAILGUN_DOMAIN_NAME:str
    MAILGUN_POSTMASTER:str
    MAILGUN_YOU: str

    model_config = SettingsConfigDict(env_file=ENV_FILE)
