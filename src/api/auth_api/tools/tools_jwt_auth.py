from typing import Annotated
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt.exceptions import InvalidTokenError

from core.models import db_helper
from core.schemas.user import UserRead
from crud import auth as auth_crud
from auth import tools as auth_tools
from crud import users as users_crud

# получаем токен из запроса в заголовке Authorization
http_bearer = HTTPBearer()

# помощник, заменяет HTTPBearer, где tokenUrl указывает на то, как мы выпускаем токен(по какому адресу будет выпускаться)
# теперь мы не выпускаем токен вручную и не вставляем его потом в отдельное поле как это было с HTTPBearer()
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/jwt-auth/login")

async def validate_auth_user(
    username : str = Form(),
    password : str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid username or password",
    )
    if not (user := await auth_crud.get_data_by_username(username)):
        raise unauthed_exc
    
    if not auth_tools.compare_hashed_passwords(
        password.encode('utf-8'),
        user.password.encode('utf-8')
    ):
        raise unauthed_exc
    return user


def get_jwt_token(
    # credentials : HTTPAuthorizationCredentials = Depends(http_bearer),
    token : str = Depends(oauth2_schema),
) -> dict:
    # token = credentials.credentials
    try:
        payload = auth_tools.decode_jwt(jwt_token=token)
    except InvalidTokenError as e: # может быть такое что токен содержит меньше сегментов в payload чем расчитано
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid to decode token."
        )
    return payload

async def get_current_active_auth_user(
    payload : dict = Depends(get_jwt_token),
    session : AsyncSession = Depends(db_helper.session_getter),     
) -> UserRead:
    id : int | None = int(payload.get('sub'))
    if not (user := await users_crud.get_user_by_id(id, session)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid token."
        )
    return user