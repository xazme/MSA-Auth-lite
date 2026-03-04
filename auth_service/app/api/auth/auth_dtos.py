from uuid import UUID
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr


class LoginDTO(BaseModel):
    email: Annotated[
        EmailStr,
        Field(..., description="User email"),
    ]
    password: Annotated[
        str,
        Field(..., description="User password"),
    ]


class RegisterDTO(LoginDTO):
    name: Annotated[
        str,
        Field(..., description="User name"),
    ]


class LogOutDTO(BaseModel):
    user_id: Annotated[
        UUID,
        Field(..., description="User name"),
    ]


class ResponseAuthTokensDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class RefreshTokenDTO(BaseModel):
    refresh_token: Annotated[
        str,
        Field(..., description="User password"),
    ]
