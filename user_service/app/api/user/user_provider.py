from faststream.kafka import KafkaBroker
from dishka import Provider, Scope, provide  # type: ignore[misc]
from sqlalchemy.ext.asyncio import AsyncSession
from .user_repository import UserRepository
from .user_service import UserService
from .user_producer import UserKafkaProducer


class UserProvider(Provider):

    @provide(scope=Scope.APP)
    def user_kafka_producer(
        self,
        broker: KafkaBroker,
    ) -> UserKafkaProducer:
        return UserKafkaProducer(
            broker=broker,
        )

    @provide(scope=Scope.REQUEST)
    def user_repository(
        self,
        session: AsyncSession,
    ) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def user_service(
        self,
        user_repository: UserRepository,
        producer: UserKafkaProducer,
        session: AsyncSession,
    ) -> UserService:
        return UserService(
            producer=producer,
            repository=user_repository,
            session=session,
        )
