from dishka import make_async_container
from app.infastructure.database import DataBaseProvider
from app.infastructure.kafka import KafkaProvider
from app.api.user.user_provider import UserProvider

container = make_async_container(
    DataBaseProvider(),
    KafkaProvider(),
    UserProvider(),
)
