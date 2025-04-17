from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

from core.config import settings

class Base(DeclarativeBase):
    __abstract__ = True

    # переопределяю метаданные базового класса для автоматического создания имен для констраинтов(ограничений)
    metadata = MetaData(
        naming_convention = settings.db.naming_convention
    )

