from typing import Any
from fastapi import APIRouter, HTTPException, Depends
from schemas import schema
from utils import customers as users_utils
from fastapi.security import OAuth2PasswordRequestForm
from core.auth import authenticate, create_access_token
from core.security import password_valid
from utils import deps
from utils.mailutils import (
    generate_password_reset_token,
    send_reset_password_email,
    # verify_password_reset_token,
)


router = APIRouter()


@router.get("/", status_code=200)
async def read_root():
    return {"Hello": "World"}


@router.post("/sign-up", response_model=schema.Customer)
async def create_user(customer: schema.CustomerCreate):
    """ create new customer """
    db_user = await users_utils.get_user_by_phonemail(email=customer.email, phone=customer.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Email or phone already registered")
    passwdvalid = password_valid(passwd=customer.password)
    if not passwdvalid:
        raise HTTPException(
            status_code=400, 
            detail="Пароль должен состоять не менее, чем из 8 знаков, "
            "содержать минимум одну заглавную букву и одну цифру")
    return await users_utils.create_user(user=customer)


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    user = await authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schema.User)
def read_users_me(current_user: schema.User = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user


# mail functions not tested yet
# to enable mail dev server:
# python -m smtpd -c DebuggingServer -n localhost:8025
@router.post("/password-recovery/{email}", response_model=schema.Msg)
async def recover_password(email: str) -> Any:
    """
    Password Recovery
    """
    user = await users_utils.get_user_by_phonemail(email=email, phone=None)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    print(password_reset_token)
    send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}