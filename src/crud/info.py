from typing import Annotated, Sequence
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload # для того, чтобы подгрузить связанные данные(часто применяется для связи ...-к-одному)
from sqlalchemy.orm import selectinload # для того, чтобы подгрузить связанные данные(часто применяется для связи ...-ко-многим)
# если делать связи ...-ко-многим через joinedload, то надо применять к результату .unique()

from core.models import InfoUser
from core.models.user import User
from core.schemas.info import InfoCreate, InfoRead
from core.schemas.info_and_user import InfoWithUser

async def get_all_infos(session : AsyncSession) -> Sequence[InfoUser]:
    stmt = select(InfoUser).options(joinedload(InfoUser.user)).order_by(InfoUser.id)
    result = await session.scalars(stmt)
    return result.all()

async def get_info_by_id(
        info_id : int,
        session : AsyncSession,
) -> InfoRead | None:
    stmt = select(InfoUser).where(InfoUser.id == info_id).options(joinedload(InfoUser.user)).order_by(InfoUser.id)
    result = await session.execute(stmt)
                # используем scalars так как нам возвращается только одна модель(InfoUser)/строки с первым значением каждой строки
    return result.scalars().one_or_none()

async def get_info_by_user_id(
        user_id : int,
        session : AsyncSession,
) -> InfoWithUser | None:
# .join уже нужен для того, чтобы работать с уже подгруженными данными(фильтровать по ним), в то время как в .options мы просто подгружаем данные(для самого ORM, а не таблиц)
    stmt = select(InfoUser).join(InfoUser.user).options(joinedload(InfoUser.user)).where(User.id == user_id).order_by(InfoUser.id)
    result = await session.execute(stmt)
                # используем scalars так как нам возвращается только одна модель(InfoUser)/строки с первым значением каждой строки
    return result.scalars().one_or_none()

async def create_info(
    info_create : InfoCreate,
    session : AsyncSession,
) -> InfoRead:
    info = InfoUser(**info_create.model_dump())
    session.add(info)
    await session.commit()
    await session.refresh(info) # чтобы в случае, когда данные одновременно достаются, обеспечить актуальность данных
    return info

async def delete_info_by_id(
        info_id : int,
        session : AsyncSession,
) -> None:
    stmt = delete(InfoUser).where(InfoUser.id==info_id)
    await session.execute(stmt)
    await session.commit()
