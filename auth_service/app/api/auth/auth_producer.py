from typing import Any
from uuid import UUID
from faststream.kafka import KafkaBroker


class AuthKafkaProducer:
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

    async def publish_create(
        self,
        payload: Any,
        user_id: UUID,
    ) -> None:
        await self._create_publisher.publish(
            message=payload,
            key=user_id.bytes,
        )
