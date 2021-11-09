from typing import Optional
from models.database import database
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel

from core.auth import oauth2_scheme
from core.config import settings
from models.customers import customers_table


class TokenData(BaseModel):
    username: Optional[str] = None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    query = customers_table.select().where(customers_table.c.id == token_data.username)
    user = await database.fetch_one(query)
    if user is None:
        raise credentials_exception
    return user
