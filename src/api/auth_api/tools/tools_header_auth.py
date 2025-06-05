# для примера, в реальном приложении логин и пароль будут храниться в базе данных
from fastapi import HTTPException, Header, status


static_auth_token_to_username = {
    "1234567890abcdef": "admin",
    "abcdef1234567890": "john",
}

def get_username_by_static_auth_token(
    static_token: str = Header(alias = "X-static-auth-token"),
) -> str:
    if static_token not in static_auth_token_to_username:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid static auth token",
            headers = {"WWW-Authenticate": "Static"},
        )
    return static_auth_token_to_username[static_token]