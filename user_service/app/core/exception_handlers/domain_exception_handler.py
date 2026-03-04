import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import DomainBaseException

logger = logging.getLogger(__name__)


def domain_exceptions_handler(
    request: Request,
    exc: DomainBaseException,
) -> JSONResponse:
    logger.warning(
        msg="Domain Exception",
        extra={
            "path": request.url.path,
            "error_type": getattr(exc, "error_type", "domain_error"),
            "error_message": exc.message,
            "details": exc.details,
        },
    )
    return JSONResponse(
        status_code=getattr(exc, "status_code", 500),
        content={
            "error_type": getattr(exc, "error_type", "domain_error"),
            "error_message": exc.message,
            "details": exc.details,
        },
    )
