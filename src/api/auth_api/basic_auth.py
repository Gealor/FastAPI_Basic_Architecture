import secrets
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from api.auth_api.tools import get_auth_username, get_username_by_static_auth_token
from api.auth_api.tools import security
# HTTPBasicCredentials - это простая pydantic модель
# HTTPBasic - это класс, который реализует HTTP Basic Authentication
# после этого

router = APIRouter()


# логин и пароль будут зашифрованы в заголовке запроса в формате base64, при раскодировании получим строку вида "username:password"
# пускаем всех подряд
@router.get('/basic-auth-free')
async def basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message" : "Hi!",
        "username": credentials.username,
        "password": credentials.password,
    }


# аутентификация по username и password, т.е. не пускать кого попало, а только тех, кто есть в базе данных
@router.get('/basic-auth-protected')
async def basic_auth_username(
    auth_username : str = Depends(get_auth_username),
):
    return {
        "message": f"Hi, {auth_username}!",
        "username": auth_username,
    }


