from dishka import make_async_container
from app.api.user.user_provider import UserProvider
from app.api.auth.auth_provider import AuthProvider
from app.api.token.token_provider import TokenProvider

from app.infastructure.jwt.jwt_provider import JWTProvider
from app.infastructure.security.password_hasher_provider import PasswordHasherProvider
from app.infastructure.database.db_provider import DataBaseProvider
from app.infastructure.kafka.kafka_provider import KafkaProvider

container = make_async_container(
    DataBaseProvider(),
    KafkaProvider(),
    UserProvider(),
    AuthProvider(),
    TokenProvider(),
    JWTProvider(),
    PasswordHasherProvider(),
)
