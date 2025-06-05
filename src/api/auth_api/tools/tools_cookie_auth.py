# временно хранилище для куки, по хорошему должно быть в базе данных или в другом хранилище
from typing import Optional
import uuid

from fastapi import Cookie, HTTPException, status


COOKIES = {}

COOKIE_SESSION_ID_KEY = "web-app-session-id" # ключ для куки, который будет хранить идентификатор сессии пользователя
# можно задать любой строкой

def generate_session_id() -> str:
    return uuid.uuid4().hex

def get_session_data(
    session_id: Optional[str] = Cookie(alias=COOKIE_SESSION_ID_KEY) # получаем значение куки по ключу COOKIE_SESSION_ID_KEY
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid session ID",
            headers = {"WWW-Authenticate": "Cookie"},
        )
    return COOKIES[session_id]