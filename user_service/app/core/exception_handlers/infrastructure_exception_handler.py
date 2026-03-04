import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import InfrastructureBaseException

logger = logging.getLogger(__name__)


def infrastructure_exceptions_handler(
    request: Request,
    exc: InfrastructureBaseException,
) -> JSONResponse:
    logger.error(
        msg="Infrastructure Exception",
        extra={
            "path": request.url.path,
            "error_type": "infrastructure_error",
            "error_message": exc.message,
            "details": exc.details,
            "model_name": exc.model_name,
        },
    )

    return JSONResponse(
        status_code=getattr(exc, "status_code", 500),
        content={
            "error_type": "infrastructure_error",
            "error_message": exc.message,
            "details": exc.details,
            "model_name": exc.model_name,
        },
    )
