from faststream.kafka import KafkaBroker
from app.core.ioc import init_faststream_ioc
from app.api import init_consumers


def create_faststream(broker: KafkaBroker):
    init_faststream_ioc(broker=broker)
    init_consumers(broker=broker)
