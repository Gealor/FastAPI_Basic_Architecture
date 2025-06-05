import datetime
import secrets
from typing import Annotated
from fastapi import APIRouter, Cookie, Depends, HTTPException, Header, Response, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from api.auth_api.tools import COOKIE_SESSION_ID_KEY, COOKIES, generate_session_id, get_auth_username, get_session_data
# HTTPBasicCredentials - это простая pydantic модель
# HTTPBasic - это класс, который реализует HTTP Basic Authentication

router = APIRouter()


@router.post('/login-cookie')
async def auth_login_cookie(
    response: Response, # объект ответа, который мы будем модифицировать
    auth_username: str = Depends(get_auth_username),
): 
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": datetime.datetime.now().ctime(),
    }
    response.set_cookie(
        key = COOKIE_SESSION_ID_KEY,
        value = session_id,
    )
    return {"result" : "ok"}


@router.get('/check-cookie')
async def auth_check_cookie(
    user_session_data : dict = Depends(get_session_data)
):
    username = user_session_data["username"]
    return {
        "message": f"Hello, {username}!",
        **user_session_data,
    }

@router.get('/logout-cookie')
async def auth_logout_cookie(
    response: Response, # объект ответа, чтобы удалить куки из ответа 
    session_id : str = Cookie(alias = COOKIE_SESSION_ID_KEY),
    user_session_data : dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    del COOKIES[session_id]
    response.delete_cookie(
        key = COOKIE_SESSION_ID_KEY
    )
    return {
        "message": f"Goodbye, {username}",
    }