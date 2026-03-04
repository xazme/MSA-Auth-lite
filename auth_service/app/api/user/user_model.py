from typing import TYPE_CHECKING
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infastructure.database import Base, CreatedAtMixin, UpdatedAtMixin
from .user_enums import UserRole

if TYPE_CHECKING:
    from app.api.token import Token


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
        default=UserRole.USER,
    )

    # relationships
    token: Mapped["Token"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
    )
