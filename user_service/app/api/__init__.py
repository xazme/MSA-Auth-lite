from faststream.kafka import KafkaBroker
from fastapi import FastAPI, APIRouter
from .health_check.health_check_router import router as health_check_router
from .user.user_router import router as user_router
from .user.user_consumer import router as user_consumer_router

router = APIRouter(prefix="/api")

router.include_router(
    router=user_router,
    prefix="/user-service",
    tags=["User"],
)
router.include_router(
    router=health_check_router,
    tags=["Health Check"],
)


def init_routers(
    app: FastAPI,
) -> None:
    app.include_router(router=router)


def init_consumers(
    broker: KafkaBroker,
) -> None:
    broker.include_router(router=user_consumer_router)


__all__ = [
    "init_routers",
    "init_consumers",
]
