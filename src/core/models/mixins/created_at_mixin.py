
from datetime import datetime, timezone
from sqlalchemy import TIMESTAMP, DateTime, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

class CreatedAtMixin:
    created_at : Mapped[datetime] = mapped_column(
        default = lambda : datetime.now(tz=timezone.utc).replace(tzinfo=None), 
        server_default=func.now(), 
        nullable = False
    ) 