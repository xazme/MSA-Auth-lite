from functools import cached_property
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from ..constans import ENV_FILE_PATH


class DataBaseConfig(BaseSettings):
    postgres_host: str = Field(
        default="localhost",
    )
    postgres_port: int = Field(
        default=5432,
    )
    postgres_user: str = Field(
        default="postgres",
    )
    postgres_password: str = Field(
        default="postgres",
    )
    postgres_db: str = Field(
        default="postgres",
    )

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
    )

    @computed_field(return_type="str")
    @cached_property
    def postgres_connection(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
