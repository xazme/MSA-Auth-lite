from functools import cached_property
from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from ..constans import ENV_FILE_PATH


class JWTConfig(BaseSettings):
    algorithm: str = Field(
        default="RS256",
        alias="jwt_algorithm",
    )
    expire_days: int = Field(
        default=0,
        alias="jwt_expire_days",
    )
    expire_minutes: int = Field(
        default=0,
        alias="jwt_expire_minutes",
    )
    access_private_key_path: str = Field(
        default="path",
        alias="jwt_access_private_key_path",
    )
    access_public_key_path: str = Field(
        default="path",
        alias="jwt_access_public_key_path",
    )
    refresh_private_key_path: str = Field(
        default="path",
        alias="jwt_refresh_private_key_path",
    )
    refresh_public_key_path: str = Field(
        default="path",
        alias="jwt_refresh_public_key_path",
    )

    # We rarely change access/refresh keys. Why not cache the property?
    @computed_field(return_type="str")
    @cached_property
    def access_private_key(self):
        with open(file=self.access_private_key_path, mode="r") as file:
            key = file.read()
        return key

    @computed_field(return_type="str")
    @cached_property
    def access_public_key(self):
        with open(file=self.access_public_key_path, mode="r") as file:
            key = file.read()
        return key

    @computed_field(return_type="str")
    @cached_property
    def refresh_private_key(self):
        with open(file=self.refresh_private_key_path, mode="r") as file:
            key = file.read()
        return key

    @computed_field(return_type="str")
    @cached_property
    def refresh_public_key(self):
        with open(file=self.refresh_public_key_path, mode="r") as file:
            key = file.read()
        return key

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
    )
