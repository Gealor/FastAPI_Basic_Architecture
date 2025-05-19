from typing import Annotated, Optional
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.schemas.error import ErrorResponse
from core.schemas.info_and_user import UserWithInfo
from core.schemas.user import UserCreate, UserDelete, UserNameMail, UserRead
from crud.users import delete_user_by_id, get_all_users, get_name_mail_by_id, get_user_by_id
from crud import users as users_crud
from core.models import db_helper


router = APIRouter(tags = ["Users"])

@router.get("/with_info")
async def get_users_with_info(
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)], 
) -> list[UserWithInfo] | ErrorResponse:
    users = await users_crud.get_users_with_info(session)
    print(users)
    if users is None:
        return {"msg" : "Пользователь не найден"}
    return users

@router.get("/with_info/{user_id}")  # параметр пути
async def get_user_with_info_by_id(
    user_id : int,
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)], 
) -> Optional[UserWithInfo] | ErrorResponse: 
    users = await users_crud.get_user_by_id_with_info(user_id, session)
    print(users)
    if users is None:
        return {"msg" : "Пользователь не найден"}
    return users

@router.get("/{user_id}")  # параметр пути
async def get_users_by_id(
    user_id : int,
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)], 
) -> UserNameMail | ErrorResponse: 
    users = await get_name_mail_by_id(user_id, session)
    print(users)
    if users is None:
        return {"msg" : "Пользователь не найден"}
    return users

@router.get("/")
async def get_users(
    # Depends используется вместе с аннотацией типов Annotated
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)],
    id : Optional[int] = None,
    # session: AsyncSession = Depends(db_helper.session_getter),
) -> list[UserRead] | UserRead | ErrorResponse:
    users = await get_all_users(session = session) if id is None else await get_user_by_id(id, session)
    if users is None:
        return {"msg" : "Пользователь не найден"}
    print(users)
    return users


@router.post("/post_user")
async def create_user(
    # чтобы были поля ввода ввожу Annotated с пустой зависимостью Depends
    user_create: Annotated[UserCreate, Depends()],  # тело запроса(Body Parameters) заменилось на параметры запроса!!!!
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)]
    # session: AsyncSession = Depends(db_helper.session_getter)
) -> UserRead:
    user = await users_crud.create_user(user_create, session)
    return user

@router.delete("/delete_user")
async def delete_user(
    user_id : int,
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> UserDelete:
    await delete_user_by_id(user_id, session)
    return {"deleted" : user_id}

