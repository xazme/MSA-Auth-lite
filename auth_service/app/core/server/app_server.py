from fastapi import FastAPI
from app.core.config import settings
from app.api import init_routers
from app.core.middlewares import init_middlewares
from app.core.ioc import init_fastapi_ioc
from app.core.exception_handlers import init_exception_handlers
from .lifespan import app_lifespan


def create_app() -> FastAPI:
    app = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        lifespan=app_lifespan,
        docs_url=settings.docs_url,
        redoc_url=settings.redoc_url,
    )
    init_fastapi_ioc(app=app)
    init_middlewares(app=app)
    init_routers(app=app)
    init_exception_handlers(app=app)
    return app


app = create_app()
