from typing import TYPE_CHECKING # флаг для избежания циклической зависимости

from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins.int_id_pk import IntIdPkMixin
from .base import Base

if TYPE_CHECKING:
    from .user import User  # импортируем только для аннотации типов, чтобы избежать циклической зависимости

class InfoUser(IntIdPkMixin, Base):
    __tablename__ = "info_users"

    user_id : Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    foo : Mapped[Optional[int]]
    baz : Mapped[Optional[int]]
# back_populates указывает на то, с какого поля в другой модели будет происходить обратная связь(т.е. с какого поля в другой модели будет происходить связь с этой моделью)
    user : Mapped["User"] = relationship(back_populates="info_user")
