from typing import MutableMapping, List, Union
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy import or_
from models.customers import customers_table
from core.config import settings
from core.security import verify_password
from models.database import database

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/login")


# для аутентификации используем email или пароль
async def authenticate(username: str, password: str):
    query = customers_table.select().where(
        or_(customers_table.c.email == username, customers_table.c.phone == username)
        )
    customer = await database.fetch_one(query)
    if not customer:
        return None
    if not verify_password(password, customer.hashed_password):  # 1
        return None
    return customer


async def create_access_token(sub: str) -> str:  # 2
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire  # 4
    payload["iat"] = datetime.utcnow()  # 5
    payload["sub"] = str(sub)  # 6

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
