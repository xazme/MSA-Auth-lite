import uvicorn

from app.core.config import settings
from app.core.logger import init_logger


def main() -> None:
    init_logger()
    uvicorn.run(
        app="app.core.server:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.reload,
        workers=settings.workers,
    )


# find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
if __name__ == "__main__":
    main()
