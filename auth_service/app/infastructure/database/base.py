import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from .db_util import generate_correct_spelling_table_name


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[uuid.UUID] = mapped_column(
        type_=UUID(as_uuid=True),
        unique=True,
        nullable=False,
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )

    @declared_attr.directive
    def __tablename__(cls):
        return generate_correct_spelling_table_name(
            name=cls.__name__.lower(),
        )
