from dishka.integrations.faststream import setup_dishka as faststream_setup_dishka
from dishka.integrations.fastapi import setup_dishka as fastapi_setup_dishka
from fastapi import FastAPI
from faststream.kafka import KafkaBroker
from .build_ioc import container


def init_fastapi_ioc(
    app: FastAPI,
) -> None:
    fastapi_setup_dishka(container=container, app=app)


def init_faststream_ioc(
    broker: KafkaBroker,
) -> None:
    faststream_setup_dishka(container=container, broker=broker)


__all__ = [
    "init_fastapi_ioc",
    "init_faststream_ioc",
]
