from sqlalchemy import or_, sql
from models.database import database
from models.customers import customers_table
from schemas import schema as user_schema
from core.security import get_password_hash
from core.auth import create_access_token
from typing import Optional


async def get_user_by_phonemail(email: str, phone: Optional[str] = None):
    """ Возвращает информацию о пользователе """
    if phone:
        query = customers_table.select().where(
            or_(customers_table.c.email == email, customers_table.c.phone == phone)
            )
    else:
        query = customers_table.select().where(
            or_(customers_table.c.email == email, customers_table.c.phone == email)
            )
    return await database.fetch_one(query)


async def create_user(user: user_schema.CustomerCreate):
    """ Создает нового пользователя в БД """
    passhash = get_password_hash(user.password)
    query = customers_table.insert().values(
        email=user.email,
        phone=user.phone,
        first_name=user.first_name,
        last_name=user.last_name,
        patronymic=user.patronymic,
        hashed_password=passhash,
    )
    user_id = await database.execute(query)

    tokenhash = await create_access_token(sub=user_id)
    return {**user.dict(), "id": user_id, "is_active": True, "token": tokenhash}


async def update_user_password(email: str, hashed_password: str):
    query = customers_table.update().where(
        customers_table.c.email == email
        ).values(hashed_password=hashed_password)
    return await database.execute(query)


async def activate_customer_account(email: str):
    query = customers_table.update().where(
        customers_table.c.email == email
        ).values(is_active=sql.expression.true())
    return await database.execute(query)
