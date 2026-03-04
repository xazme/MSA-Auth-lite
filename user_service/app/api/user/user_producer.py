from uuid import UUID
from faststream.kafka import KafkaBroker
from .user_events import UserUpdateEvent


class UserKafkaProducer:
    def __init__(
        self,
        broker: KafkaBroker,
    ) -> None:
        self._create_publisher = broker.publisher(
            topic="user-create",
        )
        self._update_publisher = broker.publisher(
            topic="user-update",
        )

    async def publish_update(
        self,
        payload: UserUpdateEvent,
        user_id: UUID,
    ) -> None:
        await self._update_publisher.publish(
            message=payload,
            key=user_id.bytes,
        )
