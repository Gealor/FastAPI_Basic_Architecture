from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint

from .base import Base

class User(Base):
    __tablename__ = "users"

    username : Mapped[str] = mapped_column(unique = True)
    mail : Mapped[str] = mapped_column(unique = True)
    foo : Mapped[int]
    baz : Mapped[int]

    # __table_args__ = (
    #     # foo и baz образовывают в совокупности уникальную комбинацию для каждой строки
    #     UniqueConstraint("foo", "baz"),
    # )