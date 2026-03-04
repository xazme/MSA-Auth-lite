from faststream.kafka import KafkaBroker
from dishka import Provider, Scope, provide  # type: ignore[misc]
from .kafka_broker import create_kafka_broker


class KafkaProvider(Provider):

    @provide(scope=Scope.APP)
    async def kafka_broker(
        self,
    ) -> KafkaBroker:
        return create_kafka_broker()
