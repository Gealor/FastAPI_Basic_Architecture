from typing import Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, db_helper
from core.schemas.user import UserRead

async def find_user_by_username(
    username : str,
    session : AsyncSession,
) -> Tuple[str] | None:
    stmt = select(User.username).where(User.username == username)

    result = await session.execute(stmt)

    return result.first()


async def get_data_by_username(
        username : str,
) -> UserRead | None:
    async with db_helper.session_factory() as session:
        stmt = select(User).where(User.username == username)
        result = await session.scalar(stmt)

    return result