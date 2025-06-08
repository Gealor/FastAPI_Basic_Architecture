from fastapi import APIRouter, Depends


from api.auth_api.tools.tools_jwt_auth import get_current_active_auth_user, validate_auth_user
from core.schemas.auth_info import TokenInfo
from core.schemas.user import UserNameMail, UserRead
from auth import tools as auth_tools

router = APIRouter(tags = ["JWT"])

@router.post('/login')
async def auth_user_jwt(
    user : UserRead = Depends(validate_auth_user)
) -> TokenInfo:
    jwt_payload = {
        # По правилу хорошего тона, в payload(данных) должен быть sub, который содержит уникальный id
        "sub" : str(user.id), # subject должен быть СТРОКОЙ
        "username" : user.username,
        "email" : user.mail,
    }
    access_token = auth_tools.encode_jwt(payload=jwt_payload)
    return TokenInfo(
        access_token=access_token,
        token_type="Bearer",
    )


@router.get('/users/me/')
async def auth_user_check_self_info(
    user : UserRead = Depends(get_current_active_auth_user)
) -> UserNameMail:
    return {
        "username" : user.username,
        "mail" : user.mail,
    }