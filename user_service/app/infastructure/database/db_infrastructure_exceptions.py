from fastapi import status
from app.core.exceptions import InfrastructureBaseException


class DBInfrastructureBaseException(InfrastructureBaseException):
    """Base class for all DB-related infrastructure exceptions"""

    ...


class DBOperationalError(DBInfrastructureBaseException):
    """Database operational error (connection issues, timeouts, locks, etc.)"""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        message: str = "Database operational error occurred",
        model_name: str | None = None,
        details: str | None = None,
    ) -> None:
        super().__init__(
            message=message,
            model_name=model_name,
            details=details,
        )


class DBDatabaseError(DBInfrastructureBaseException):
    """General database error"""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        message: str = "Database error occurred",
        model_name: str | None = None,
        details: str | None = None,
    ) -> None:
        super().__init__(
            message=message,
            model_name=model_name,
            details=details,
        )


class DBSQLAlchemyError(DBInfrastructureBaseException):
    """Generic SQLAlchemy error"""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        message: str = "SQLAlchemy internal error occurred",
        model_name: str | None = None,
        details: str | None = None,
    ) -> None:
        super().__init__(
            message=message,
            model_name=model_name,
            details=details,
        )
