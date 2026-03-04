from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from app.infastructure.database import BaseResponseMixin
from .user_enums import UserRole


class UpdateUserDTO(BaseModel):
    name: Annotated[str, Field(...)]
    email: Annotated[EmailStr, Field(...)]
    password: Annotated[str, Field(...)]


class ResponseUserDTO(BaseModel, BaseResponseMixin):
    name: str
    email: EmailStr
    password: str
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True,
    )
