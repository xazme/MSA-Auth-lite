from typing import Annotated
from fastapi import Depends, Cookie
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from .auth_exceptions import NotAuthenticatedException, EmptyTokenProvidedException

# http_bearer = HTTPBearer(auto_error=False)


# def get_access_token(
#     credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(http_bearer)],
# ) -> str:
#     if not credentials:
#         raise NotAuthenticatedException()
#     token = credentials.credentials
#     if not token:
#         raise EmptyTokenProvidedException()
#     return token


async def get_refresh_token(refresh_token: Annotated[str | None, Cookie()]) -> str:
    if not refresh_token:
        raise EmptyTokenProvidedException()
    return refresh_token


RefreshTokenDep = Annotated[str, Depends(get_refresh_token)]
