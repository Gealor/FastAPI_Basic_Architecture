# для примера, в реальном приложении логин и пароль будут храниться в базе данных
import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
# HTTPBasicCredentials - это простая pydantic модель
# HTTPBasic - это класс, который реализует HTTP Basic Authentication

security = HTTPBasic()

usernames_to_passwords = {
    "admin" : "admin",
    "john" : "password",
}

def get_auth_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    unauthed_exc = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED, # статус код ошибки
        detail = "Invalid username or password", # текст ошибки
        headers = {"WWW-Authentificate" : "Basic"} # хороший тон, указывать заголовки, чтобы браузер понял, что тут можно залогиниться по basic auth
    )
    if credentials.username not in usernames_to_passwords:
        raise unauthed_exc
    
    correct_password = usernames_to_passwords[credentials.username]
    # лучше для сравнения паролей и в принципе важных данных использовать модуль secrets, вместо == 
    if not secrets.compare_digest(
        credentials.password.encode('utf-8'),
        correct_password.encode('utf-8'),
    ):
        raise unauthed_exc
    
    return credentials.username