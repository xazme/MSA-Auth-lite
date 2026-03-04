from uuid import UUID
from typing import TYPE_CHECKING
from app.api.user.user_events import UserCreateEvent
from app.api.user.user_enums import UserRole
from app.api.user.user_service import UserService
from app.api.token.token_dto import UpsertTokenDTO
from app.api.token.token_service import TokenService
from app.infastructure.jwt import JWTHelper
from app.infastructure.security import PasswordHasher
from .auth_dtos import (
    LoginDTO,
    RegisterDTO,
    LogOutDTO,
    ResponseAuthTokensDTO,
    RefreshTokenDTO,
)
from .auth_exceptions import (
    PasswordIsIncorrectException,
    AccountAlreadyExists,
    RefreshTokenCompromisedException,
)
from .auth_producer import AuthKafkaProducer

if TYPE_CHECKING:
    from app.api.user import User


class AuthService:
    def __init__(
        self,
        jwt_helper: JWTHelper,
        password_hasher: PasswordHasher,
        token_service: TokenService,
        user_service: UserService,
        auth_kafka_producer: AuthKafkaProducer,
    ) -> None:
        self.jwt_helper = jwt_helper
        self.password_hasher = password_hasher
        self.user_service = user_service
        self.token_service = token_service
        self.auth_kafka_producer = auth_kafka_producer

    async def login(
        self,
        payload: LoginDTO,
    ) -> ResponseAuthTokensDTO:
        user_email = payload.email
        user = await self.user_service.get_one_or_none(email=user_email)

        if not user or not self.password_hasher.check(
            password=payload.password,
            password_hash=user.password,
        ):
            raise PasswordIsIncorrectException(message="Password is Incorrect")
        return await self._create_and_save_token(user=user)

    async def register(
        self,
        payload: RegisterDTO,
    ) -> ResponseAuthTokensDTO:
        existing_user = await self.user_service.get_one_or_none(email=payload.email)
        if existing_user:
            raise AccountAlreadyExists(message="Account Already Exists")

        hashed_password = self.password_hasher.get(payload.password)
        user_data = payload.model_dump()
        user_data.update(
            {
                "password": hashed_password,
                "role": UserRole.USER,
            }
        )
        user = await self.user_service.create(payload=user_data)
        await self.auth_kafka_producer.publish_create(
            payload=UserCreateEvent.model_validate(user),
            user_id=user.id,
        )
        return await self._create_and_save_token(user=user)

    async def logout(
        self,
        payload: LogOutDTO,
    ) -> None:
        await self.token_service.delete(user_id=payload.user_id)

    async def refresh_token(
        self,
        payload: RefreshTokenDTO,
    ) -> ResponseAuthTokensDTO:
        data = self.jwt_helper.decode_refresh_token(token=payload.refresh_token)
        user_id: str = data.get("user-id")  # type: ignore
        user = await self.user_service.get_one(id=user_id)
        db_token = await self.token_service.get_one_or_none(user_id=user.id)
        if (
            not db_token
            or db_token.refresh_token != payload.refresh_token
            or not db_token.refresh_token
        ):
            await self.token_service.delete(refresh_token=payload.refresh_token)
            raise RefreshTokenCompromisedException(
                message="Refresh token is invalid or has been used"
            )
        return await self._create_and_save_token(user=user)

    async def _create_and_save_token(
        self,
        user: "User",
    ) -> ResponseAuthTokensDTO:
        user_id = user.id
        jwt_payload: dict[str, UUID | str] = {
            "user-id": str(user_id),
            "role": user.role,
        }
        jwt_payload_access: dict[str, UUID | str] = {
            **jwt_payload,
            "iss": "auth-service-access",
        }
        jwt_payload_refresh: dict[str, UUID | str] = {
            **jwt_payload,
            "iss": "auth-service-refresh",
        }
        access_token = self.jwt_helper.generate_access_token(data=jwt_payload_access)
        refresh_token = self.jwt_helper.generate_refresh_token(data=jwt_payload_refresh)

        await self.token_service.upsert(
            payload=UpsertTokenDTO(user_id=user_id, refresh_token=refresh_token)
        )
        return ResponseAuthTokensDTO(
            access_token=access_token,
            refresh_token=refresh_token,
        )

    async def get_user_from_access_token(
        self,
        access_token: str,
    ) -> "User":
        payload = self.jwt_helper.decode_access_token(token=access_token)
        user_id: str = payload.get("user_id")  # type: ignore
        user: "User" = await self.user_service.get_one(id=UUID(user_id))
        return user
