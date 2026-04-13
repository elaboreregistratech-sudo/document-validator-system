from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Document Validator System"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    secret_key: str = "change-this-secret-key"
    access_token_expire_minutes: int = 120
    database_url: str = "sqlite:///./document_validator.db"
    default_admin_email: str = "admin@legaltech.local"
    default_admin_password: str = "Admin@123"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
