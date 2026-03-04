from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        type_=DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),
    )


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        type_=DateTime(timezone=True),
        nullable=False,
        index=True,
        onupdate=func.now(),
        server_default=func.now(),
    )
