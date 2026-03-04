from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Body, status, Response
from typing import Annotated
from .auth_service import AuthService
from .auth_dtos import (
    LoginDTO,
    RegisterDTO,
    # LogOutDTO,
    ResponseAuthTokensDTO,
    RefreshTokenDTO,
)
from .auth_dependencies import RefreshTokenDep

router = APIRouter()


@router.post(
    path="/login",
    response_model=ResponseAuthTokensDTO,
    response_model_exclude={"refresh_token"},
    status_code=status.HTTP_200_OK,
)
@inject
async def login(
    response: Response,
    payload: Annotated[LoginDTO, Body(...)],
    auth_service: FromDishka[AuthService],
):
    tokensDTO = await auth_service.login(payload=payload)
    response.set_cookie(
        key="refresh_token",
        value=tokensDTO.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,  # FIXME
    )
    return tokensDTO


@router.post(
    path="/register",
    response_model=ResponseAuthTokensDTO,
    response_model_exclude={"refresh_token"},
    status_code=status.HTTP_201_CREATED,
)
@inject
async def register(
    response: Response,
    payload: Annotated[RegisterDTO, Body(...)],
    auth_service: FromDishka[AuthService],
):
    tokensDTO = await auth_service.register(payload=payload)
    response.set_cookie(
        key="refresh_token",
        value=tokensDTO.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )
    return tokensDTO


# @router.delete(
#     path="/logout",
#     response_model=None,
#     status_code=status.HTTP_204_NO_CONTENT,
# )
# @inject
# async def logout(
#     response: Response,
#     auth_service: FromDishka[AuthService],
# ):
#     await auth_service.logout(payload=LogOutDTO(user_id=user.id))
#     response.delete_cookie(key="refresh_token")


@router.post(
    path="/refresh",
    response_model=ResponseAuthTokensDTO,
    status_code=status.HTTP_200_OK,
)
@inject
async def refresh(
    response: Response,
    refresh_token: RefreshTokenDep,
    auth_service: FromDishka[AuthService],
):
    tokensDTO = await auth_service.refresh_token(
        payload=RefreshTokenDTO(refresh_token=refresh_token)
    )
    response.set_cookie(
        key="refresh_token",
        value=tokensDTO.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=604800,
    )
    return tokensDTO
