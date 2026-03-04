from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.infastructure.database import Base, CreatedAtMixin, UpdatedAtMixin
from .user_enums import UserRole


class User(Base, CreatedAtMixin, UpdatedAtMixin):
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, create_type=False),
        nullable=False,
    )
