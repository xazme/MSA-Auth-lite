import jwt
from typing import Any, Optional
from datetime import datetime, timedelta, timezone
from jwt.exceptions import (
    PyJWTError,
    InvalidSignatureError,
    ExpiredSignatureError,
    DecodeError,
    InvalidAlgorithmError,
    ImmatureSignatureError,
    InvalidAudienceError,
)
from .jwt_enums import TokenType
from .jwt_exceptions import JWTExpiredError, JWTInvalidError


class JWTHelper:
    def __init__(
        self,
        alogrithm: str,
        expire_days: int,
        expire_minutes: int,
        access_public_key: str | bytes,
        refresh_public_key: str | bytes,
        access_private_key: str | bytes,
        refresh_private_key: str | bytes,
    ):
        self.alogrithm = alogrithm
        self.expire_days = expire_days
        self.expire_minutes = expire_minutes
        self.access_public_key = access_public_key
        self.refresh_public_key = refresh_public_key
        self.access_private_key = access_private_key
        self.refresh_private_key = refresh_private_key

    def generate_access_token(
        self,
        data: dict[str, Any],
    ) -> str:
        token = self.__encode(
            data=data,
            algorithm=self.alogrithm,
            private_key=self.access_private_key,
            expire_minutes=self.expire_minutes,
        )
        return token

    def generate_refresh_token(
        self,
        data: dict[str, Any],
    ) -> str:
        token = self.__encode(
            data=data,
            algorithm=self.alogrithm,
            private_key=self.refresh_private_key,
            expire_days=self.expire_days,
        )
        return token

    def decode_access_token(
        self,
        token: str,
    ) -> Optional[dict[str, Any]]:
        return self.__decode(
            token=token,
            type=TokenType.ACCESS,
        )

    def decode_refresh_token(
        self,
        token: str,
    ) -> Optional[dict[str, Any]]:
        return self.__decode(
            token=token,
            type=TokenType.REFRESH,
        )

    def __decode(
        self,
        token: str,
        type: TokenType,
    ) -> Optional[dict[str, Any]]:
        key = (
            self.access_public_key
            if type == TokenType.ACCESS
            else self.refresh_public_key
        )
        try:
            data = jwt.decode(
                jwt=token,
                algorithms=[self.alogrithm],
                key=key,
            )
            return data
        except ExpiredSignatureError:
            raise JWTExpiredError("Token expired")
        except (
            InvalidSignatureError,
            DecodeError,
            InvalidAlgorithmError,
            ImmatureSignatureError,
            InvalidAudienceError,
        ):
            raise JWTInvalidError("Invalid token")
        except PyJWTError as e:
            raise JWTInvalidError(f"Token error: {str(e)}")

    def __encode(
        self,
        data: dict[str, Any],
        algorithm: str,
        private_key: str | bytes,
        expire_minutes: int | None = None,
        expire_days: int | None = None,
    ) -> str:
        now = datetime.now(timezone.utc)

        if expire_minutes:
            exp = now + timedelta(minutes=expire_minutes)
        elif expire_days:
            exp = now + timedelta(days=expire_days)
        else:
            exp = now + timedelta(days=1)

        data_to_encode = data.copy()
        data_to_encode.update(
            exp=exp,
            iat=now,
        )
        return jwt.encode(
            payload=data_to_encode,
            key=private_key,
            algorithm=algorithm,
        )
