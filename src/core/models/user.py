from typing import Optional, TYPE_CHECKING  # флаг для избежания циклической зависимости
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, UniqueConstraint

from .mixins.created_at_mixin import CreatedAtMixin
from .mixins.int_id_pk import IntIdPkMixin

from .base import Base

if TYPE_CHECKING:
    from .info import InfoUser

class User(IntIdPkMixin, CreatedAtMixin, Base):
    __tablename__ = "users"

    username : Mapped[str] = mapped_column(unique = True)
    mail : Mapped[str] = mapped_column(unique = True)
                                               # server_default для заполнения этого столбца всех строк указанным значением
    password : Mapped[str] = mapped_column(default = True, server_default="password_test", nullable=False)
# back_populates указывает на то, с какого поля в другой модели будет происходить обратная связь(т.е. с какого поля в другой модели будет происходить связь с этой моделью)
    info_user : Mapped[Optional["InfoUser"]] = relationship(back_populates="user", cascade="all, delete-orphan")
# cascade = "all, delete" нужно, чтобы при удалении записи из users удалялись связанные с этой записью строки из связанной таблицы
    # __table_args__ = (
    #     # foo и baz образовывают в совокупности уникальную комбинацию для каждой строки
    #     UniqueConstraint("foo", "baz"),
    # )