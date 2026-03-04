from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from ..constans import ENV_FILE_PATH


class PGAdminConfig(BaseSettings):
    pg_admin_email: str = Field(default="111")
    pg_admin_password: str = Field(default="111")
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
    )
