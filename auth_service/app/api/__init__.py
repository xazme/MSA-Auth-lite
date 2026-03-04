from faststream.kafka import KafkaBroker
from fastapi import FastAPI, APIRouter
from .auth.auth_router import router as auth_router

# from .auth.auth_consumer import router as auth_consumer_router

router = APIRouter(prefix="/api")

router.include_router(
    router=auth_router,
    prefix="/auth-service",
    tags=["User"],
)


def init_routers(
    app: FastAPI,
) -> None:
    app.include_router(router=router)


def init_consumers(
    broker: KafkaBroker,
) -> None:
    # broker.include_router(router=user_consumer_router)
    pass


__all__ = [
    "init_routers",
    "init_consumers",
]
