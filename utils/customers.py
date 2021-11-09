from sqlalchemy import or_
from typing import Optional
from models.database import database
from models.customers import customers_table
from schemas import schema as user_schema
from core.security import get_password_hash
from core.auth import create_access_token


async def get_user_by_phonemail(email: str, phone: str):
    """ Возвращает информацию о пользователе """
    query = customers_table.select().where(or_(customers_table.c.email == email, customers_table.c.phone == phone))
    return await database.fetch_one(query)



async def create_user(user: user_schema.CustomerCreate):
    """ Создает нового пользователя в БД """
    passhash = get_password_hash(user.password)
    query = customers_table.insert().values(
        email = user.email,
        phone = user.phone,
        first_name = user.first_name,       
        last_name = user.last_name,
        patronymic = user.patronymic,
        hashed_password = passhash,
    )
    user_id = await database.execute(query)  
    tokenhash = create_access_token(sub=user_id)
    return {**user.dict(), "id": user_id, "is_active": True, "token": tokenhash}