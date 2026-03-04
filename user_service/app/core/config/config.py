import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from .constans import ENV_FILE_PATH

ENV = os.getenv("ENV", "dev")


class Config(BaseSettings):
    reload: bool = Field(default=False)
    workers: int = Field(default=8)
    docs_url: str | None = Field(default=None)
    redoc_url: str | None = Field(default=None)

    cors_origins: list[str] = Field(default=["https://givemeajobplz.com"])
    cors_allow_credentials: bool = Field(default=True)
    cors_allow_methods: list[str] = Field(default=["GET", "POST", "PUT", "DELETE"])
    cors_allow_headers: list[str] = Field(default=["*"])

    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
    )
