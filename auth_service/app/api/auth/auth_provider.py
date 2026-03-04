from faststream.kafka import KafkaBroker
from dishka import Provider, Scope, provide  # type: ignore[misc]
from app.api.token import TokenService
from app.api.user import UserService
from app.infastructure.jwt import JWTHelper
from app.infastructure.security import PasswordHasher
from .auth_producer import AuthKafkaProducer
from .auth_service import AuthService


class AuthProvider(Provider):

    @provide(scope=Scope.APP)
    def auth_kafka_producer(
        self,
        broker: KafkaBroker,
    ) -> AuthKafkaProducer:
        return AuthKafkaProducer(broker=broker)

    @provide(scope=Scope.REQUEST)
    def auth_service(
        self,
        token_service: TokenService,
        user_service: UserService,
        jwt_helper: JWTHelper,
        password_hasher: PasswordHasher,
        auth_producer: AuthKafkaProducer,
    ) -> AuthService:
        return AuthService(
            token_service=token_service,
            user_service=user_service,
            jwt_helper=jwt_helper,
            password_hasher=password_hasher,
            auth_kafka_producer=auth_producer,
        )
