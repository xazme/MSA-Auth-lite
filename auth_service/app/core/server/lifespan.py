from typing import AsyncGenerator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from faststream.kafka import KafkaBroker
from app.core.ioc import container
from app.infastructure.database import DataBaseHelper
from .broker_server import create_faststream


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    db_helper = await container.get(DataBaseHelper)
    kafka_broker = await container.get(KafkaBroker)
    create_faststream(broker=kafka_broker)
    await db_helper.create_tables()
    await kafka_broker.start()
    yield
    # TODO: remove this
    # await db_helper.drop_tables()
    await kafka_broker.stop()
