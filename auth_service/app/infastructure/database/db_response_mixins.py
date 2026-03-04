from uuid import UUID
from datetime import datetime


class CreatedAtResponseMixin:
    created_at: datetime


class UpdatedAtResponseMixin:
    updated_at: datetime


class BaseResponseMixin(CreatedAtResponseMixin, UpdatedAtResponseMixin):
    id: UUID
