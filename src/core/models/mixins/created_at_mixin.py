
from datetime import datetime
from sqlalchemy import TIMESTAMP, DateTime, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class CreatedAtMixin:
    created_at : Mapped[datetime] = mapped_column(default = datetime.now(), server_default="now()", nullable = False) 