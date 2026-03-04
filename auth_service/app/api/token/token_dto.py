from uuid import UUID
from typing import Annotated
from pydantic import BaseModel, Field


class CreateTokenDTO(BaseModel):
    user_id: Annotated[UUID, Field(default=...)]
    refresh_token: Annotated[str, Field(default=...)]


class UpdateTokenDTO(CreateTokenDTO): ...


class UpsertTokenDTO(CreateTokenDTO): ...
