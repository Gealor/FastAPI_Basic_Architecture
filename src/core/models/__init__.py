# нужно для import *(импортируются все объекты перечисленный в кортеже, т.е при from models import * импортируются все эти объекты)
__all__ = (
    "db_helper",
    "Base",
    "User"
)

from .db_helper import db_helper
from .base import Base
from .test_model import User