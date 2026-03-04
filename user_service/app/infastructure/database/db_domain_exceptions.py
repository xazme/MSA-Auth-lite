from fastapi import status
from app.core.exceptions import DomainBaseException


class DBDomainBaseException(DomainBaseException): ...


class ObjectNotFoundException(DBDomainBaseException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(
        self,
        message: str | None = None,
        details: str | None = None,
        model_name: str | None = None,
    ) -> None:
        if message is None:
            message = f"{model_name} not found"

        super().__init__(
            message=message,
            details=details,
            model_name=model_name,
        )


class ObjectAlreadyExistsException(DBDomainBaseException):
    status_code = status.HTTP_409_CONFLICT

    def __init__(
        self,
        message: str | None = None,
        details: str | None = None,
        model_name: str | None = None,
    ) -> None:
        if message is None:
            message = f"{model_name} already exists"
        super().__init__(
            message=message,
            details=details,
            model_name=model_name,
        )
