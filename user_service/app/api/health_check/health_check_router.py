from fastapi import APIRouter, status
from .health_check_dtos import ResponseHealthCheckDTO

router = APIRouter()


@router.get(
    path="/health_check",
    response_model=ResponseHealthCheckDTO,
    status_code=status.HTTP_200_OK,
)
async def get_health() -> ResponseHealthCheckDTO:
    return ResponseHealthCheckDTO(status="I'am alive")
