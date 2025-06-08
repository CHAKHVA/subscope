from pydantic import AnyHttpUrl, EmailStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Subscope"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    API_V1_STR: str = "/api/v1"
    API_PORT: int = 80

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: str

    ENVIRONMENT: str = "development"

    # CORS
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, list | str):
            return v
        raise ValueError(v)

    # Superuser
    FIRST_SUPERUSER: EmailStr = "admin@subscope.com"
    FIRST_SUPERUSER_PASSWORD: str = "admin"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
