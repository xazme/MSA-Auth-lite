from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.api.user import UserRole


class UserCreateEvent(BaseModel):
    id: UUID
    name: str
    email: str
    password: str
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserUpdateEvent(UserCreateEvent): ...
