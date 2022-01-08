from typing import Any
from core.config import settings
from fastapi import APIRouter, HTTPException, Depends, Body
from schemas import schema
from utils import customers as users_utils
from fastapi.security import OAuth2PasswordRequestForm
from core.auth import authenticate, create_access_token
from core.security import password_valid, get_password_hash
from utils import deps
from utils.mailutils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
    send_new_account_email,
)


router = APIRouter()


@router.get("/", status_code=200)
async def read_root():
    return {"Hello": "World"}


@router.post("/auth/sign-up", response_model=schema.Customer)
async def create_user(customer: schema.CustomerCreate):
    """ create new customer """
    db_user = await users_utils.get_user_by_phonemail(
        email=customer.email, phone=customer.phone
        )
    if db_user:
        raise HTTPException(status_code=400, detail="Email or phone already registered")
    passwdvalid = password_valid(passwd=customer.password)
    if not passwdvalid:
        raise HTTPException(
            status_code=400,
            detail="Пароль должен состоять не менее, чем из 8 знаков, "
            "содержать минимум одну заглавную букву и одну цифру")

    if settings.EMAILS_ENABLED and customer.email:
        token = generate_password_reset_token(email=customer.email)
        send_new_account_email(
            email_to=customer.email, username=customer.first_name, token=token
        )
    return await users_utils.create_user(user=customer)


@router.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """
    user = await authenticate(
        username=form_data.username,
        password=form_data.password
        )
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password"
            )
    return {
        "access_token": await create_access_token(sub=user.id),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schema.User)
async def read_users_me(current_user: schema.User = Depends(deps.get_current_user)):
    """
    Fetch the current logged in user.
    """

    user = current_user
    return user


@router.get("/auth/veryfy-account", response_model=schema.Msg)
async def veryfy_account(token: str) -> Any:
    """
    account verify after registration
    """
    email = verify_password_reset_token(token)
    success = await users_utils.activate_customer_account(email=email)
    if success:
        return {"msg": "Your account veryfied"}
    else:        
        raise HTTPException(
            status_code=404,
            detail="Something went wrong, try again later",)


# to enable mail dev server:
# python -m smtpd -c DebuggingServer -n localhost:8025
@router.post("/auth/password-recovery/{email}", response_model=schema.Msg)
async def recover_password(email: str) -> Any:
    """
    Password Recovery
    """
    user = await users_utils.get_user_by_phonemail(email=email)
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


@router.post("/auth/reset-password/", response_model=schema.Msg)
async def reset_password(token: str = Body(...), new_password: str = Body(...), ) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await users_utils.get_user_by_phonemail(email=email, phone=None)
    print(user)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )

    hashed_password = get_password_hash(new_password)
    print(hashed_password)
    await users_utils.update_user_password(user.email, hashed_password)
    return {"msg": "Password updated successfully"}
