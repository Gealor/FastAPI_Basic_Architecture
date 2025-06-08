from typing import Optional
from core.schemas.info import InfoBase, InfoRead
from core.schemas.user import UserBase, UserRead


class UserWithInfo(UserRead):
    info_user: Optional[InfoRead] = None # для того чтобы не было ошибки, если в базе данных нет информации о пользователе
    # объявляем так чтобы fastapi видел что эти данные подтягиваются из другой таблицы с помощью join и выдавал данные из этой таблицы

class InfoWithUser(InfoRead):
    user : Optional[UserBase] = None