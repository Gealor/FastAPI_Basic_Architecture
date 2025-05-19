from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas.error import ErrorResponse
from core.schemas.info import InfoCreate, InfoDelete, InfoRead
from core.schemas.info_and_user import InfoWithUser
from crud import info as info_crud


router = APIRouter(tags = ["Info"])

@router.get("/info_by_user_id/{user_id}")
async def get_info_by_user_id(
    user_id : int,
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> InfoWithUser | ErrorResponse:
    info = await info_crud.get_info_by_user_id(user_id, session)
    if info is None:
        return {"msg" : "Информация не найдена"}
    return info

@router.get("/{info_id}")
async def get_info_by_info_id(
    info_id : int,
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> InfoRead | ErrorResponse:
    info = await info_crud.get_info_by_id(info_id, session)
    if info is None:
        return {"msg" : "Информация не найдена"}
    return info

@router.get("/")
async def get_info(
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> list[InfoRead]:
    infos = await info_crud.get_all_infos(session = session)
    print(infos)
    return infos

@router.post("/post_info")
async def create_info(
    info_create: Annotated[InfoCreate, Depends()],  # не тело запроса, а параметры запроса
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> InfoRead:
    info = await info_crud.create_info(info_create, session)
    return info

@router.delete("/delete_info")
async def delete_info(
    info_id : int,
    session : Annotated[AsyncSession, Depends(db_helper.session_getter)]
) -> InfoDelete:
    await info_crud.delete_info_by_id(info_id, session)
    return {"deleted" : info_id}