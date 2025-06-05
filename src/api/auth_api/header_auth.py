import secrets
from typing import Annotated
from fastapi import APIRouter, Depends

from api.auth_api.tools import get_username_by_static_auth_token
# HTTPBasicCredentials - это простая pydantic модель
# HTTPBasic - это класс, который реализует HTTP Basic Authentication
# после этого

router = APIRouter()

# АВТОРИЗАЦИЯ по статическому токену, который передается в заголовке запроса
@router.get('/header-auth')
async def auth_http_header(
    auth_username : str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": f"Hi, {auth_username}!",
        "username": auth_username,
    }