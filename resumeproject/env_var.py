import os


class Settings:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    EMAIL_PORT = os.environ.get("EMAIL_PORT")
    EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
    DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")


settings = Settings()
