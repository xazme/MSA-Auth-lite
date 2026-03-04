from fastapi import status
from app.core.exceptions import DomainBaseException


class AuthBaseException(DomainBaseException): ...


class PasswordIsIncorrectException(AuthBaseException):
    """Password is incorrect"""

    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(
        self,
        message: str = "Your password is incorrect",
        details: str | None = "Perhaps you entered the wrong email?",
    ) -> None:
        super().__init__(
            message,
            details,
        )


class AccountAlreadyExists(AuthBaseException):
    """Account already exists"""

    status_code = status.HTTP_409_CONFLICT

    def __init__(
        self,
        message: str = "Account already exists",
        details: str | None = "Use other credentials",
    ) -> None:
        super().__init__(
            message,
            details,
        )


class RefreshTokenCompromisedException(AuthBaseException):
    """Refresh token is invalid or has been used"""

    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(
        self,
        message: str = "Not Authenticated",
        details: str | None = None,
    ) -> None:
        super().__init__(
            message,
            details,
        )


class NotAuthenticatedException(AuthBaseException):
    """Not Authenticated"""

    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(
        self,
        message: str = "Not Authenticated",
        details: str | None = None,
    ) -> None:
        super().__init__(
            message,
            details,
        )


class EmptyTokenProvidedException(AuthBaseException):
    """Empty token provided"""

    status_code = status.HTTP_401_UNAUTHORIZED

    def __init__(
        self,
        message: str = "Not Authenticated",
        details: str | None = None,
    ) -> None:
        super().__init__(
            message,
            details,
        )


class NotEnoughtPermissionsException(AuthBaseException):
    """Not Enough Permissions Exception"""

    status_code = status.HTTP_403_FORBIDDEN

    def __init__(
        self,
        message: str = "You dont have enought permissions for that operation",
        details: str | None = None,
    ) -> None:
        super().__init__(
            message,
            details,
        )
