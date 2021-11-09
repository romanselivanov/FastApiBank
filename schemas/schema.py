import emails
from pydantic import BaseModel, EmailStr, ValidationError, validator
from typing import Optional


class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    phone: str
    password: str

    @validator('phone')
    def validator_phone(cls, v):
        if len(v) < 5:
            raise ValueError('Phone length must be greater than 5')
        if not v.isnumeric():
            raise ValueError('Phone must contain only digits')

        return v


class Customer(BaseModel):
    """ Формирует тело ответа с деталями пользователя """
    id: int
    email: EmailStr
    first_name: str
    token: str


class UserInDBBase(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    id: Optional[int] = None


class User(UserInDBBase):
    ...


class Msg(BaseModel):
    msg: str
