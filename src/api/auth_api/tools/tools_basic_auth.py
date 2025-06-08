# для примера, в реальном приложении логин и пароль будут храниться в базе данных
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from auth import tools as auth_tools
from core.models import db_helper
from crud.auth import find_user_by_username, get_data_by_username
# HTTPBasicCredentials - это простая pydantic модель
# HTTPBasic - это класс, который реализует HTTP Basic Authentication

security = HTTPBasic()


async def get_auth_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    unauthed_exc = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED, # статус код ошибки
        detail = "Invalid username or password", # текст ошибки
        headers = {"WWW-Authentificate" : "Basic"} # хороший тон, указывать заголовки, чтобы браузер понял, что тут можно залогиниться по basic auth
    )
    
    username = await find_user_by_username(credentials.username, session)

    if username is None:
        raise unauthed_exc
    
    user_data = await get_data_by_username(credentials.username)
    # лучше для сравнения паролей и в принципе важных данных использовать модуль secrets, вместо == 
    if not auth_tools.compare_hashed_passwords(
        credentials.password.encode('utf-8'),
        user_data.password.encode('utf-8'),
    ):
        raise unauthed_exc
    
    return credentials.username