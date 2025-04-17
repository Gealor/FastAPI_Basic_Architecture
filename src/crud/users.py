import asyncio
from typing import Annotated, Sequence
from sqlalchemy import delete, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, db_helper
from core.schemas.info import InfoBase
from core.schemas.user import UserCreate, UserNameMail

async def get_all_users(session: AsyncSession) -> Sequence[User]:
    # в select указывается модель таблицы(или столбцы из таблицы), из которой нужно достать данные(обращается именно к этой таблице)
    stmt = select(User).order_by(User.id)
    # scalars используется, если нужно выбрать один столбец или целую модель
    result = await session.scalars(stmt)
    return result.all()


async def get_user_by_id(
        user_id : int,
        session : AsyncSession,
) -> UserNameMail | None:
    stmt = select(User.username, User.mail).where(User.id == user_id).order_by(User.id)
    # execute используется, если нужно выбрать несколько(больше чем 1) столбцов(как тут username и mail)
    result = await session.execute(stmt)
    return result.first() # возвращает первую строку результата запроса, если такой нет, то None


async def create_user(
        user_create : UserCreate,
        session : AsyncSession,
) -> User:
    # добавить хэширование пароля
    user = User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user) # чтобы в случае, когда данные одновременно достаются, обеспечить актуальность данных
    return user

async def delete_user_by_id(
        user_id : int,
        session : AsyncSession,
) -> None:
    stmt = select(User).options(joinedload(User.info_user)).where(User.id==user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        await session.delete(user)
        await session.commit()


async def get_users_with_info(
        session: AsyncSession,
) -> list[User]:
                        # это нужно для подгрузки данных из других таблиц, для фильтрации надо использовать .join(User.info_user)
    stmt = select(User).options(joinedload(User.info_user)).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()

async def get_user_by_id_with_info(
        user_id: int,
        session: AsyncSession,
) -> User | None:
    stmt = select(User).options(joinedload(User.info_user)).where(User.id == user_id).order_by(User.id)
    result = await session.scalars(stmt)
    return result.first()  # возвращает первую строку результата запроса, если такой нет, то None

