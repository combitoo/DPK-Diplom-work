from fastapi import APIRouter, Depends, status, Form
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException 

from typing import Optional
from datetime import timedelta
from passlib.context import CryptContext

from database.models import User

import re


router_api = APIRouter(prefix="/auth", tags=["Auth"])


SECRET = "4816ED2EFC4751897DE57615F40E0AFD0DB1CEC3130BFFF85B1A053B01549B5A"
templates = Jinja2Templates(directory="templates")

manager = LoginManager(SECRET, token_url="/auth/login", use_cookie=True)
manager.cookie_name = "BloGO-Auth"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class NotAuthenticatedException(Exception):
    pass


@manager.user_loader()
async def load_user(username: str):
    user = await User.get_or_none(username=username).only("id", "username", "role", "disabled", "description", "avatar_link")
    return user


@router_api.post("/login")
async def login(
    request: Request, 
    data: OAuth2PasswordRequestForm = Depends(),
    remember: Optional[bool] = Form(False)
):
    username = data.username
    password = data.password
    user = await load_user(username)

    errors = []

    if not user:
        errors.append("Пользователя не существует!")
    try:
        h_pwd = (await User.get_or_none(username=username)).hashed_password
        if not pwd_context.verify(password, h_pwd):
            errors.append("Неправильный пароль!")
    except:
        errors.append("Неправильный пароль!")
    
    if errors != []:
        return templates.TemplateResponse('auth/login.html', {
            "request": request,
            "errors": errors,
            "user": None,
            "email": username,
            "password": password,
        })
    
    if remember:
        access_token = manager.create_access_token(
            data={"sub": username},
            expires=timedelta(hours=48)
        )
    else:
        access_token = manager.create_access_token(
            data={"sub": username}
        )

    resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, access_token)

    return resp

@router_api.post('/registration')
async def registration(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    confirm_password: str = Form(""),
    terms: Optional[bool] = Form(False),
    remember: Optional[bool] = Form(False)
):
    user = await User.get_or_none(username=username)

    if user is not None:
        return templates.TemplateResponse('auth/registration.html', {
            "request": request,
            "errors": ["Пользователь уже существует!"],
            "user": None,
            "email": username,
            "password": password,
            "confirm_password": confirm_password,
        })
    
    errors = []

    if not re.match(r'^[a-zA-Z0-9]+$', username) or not re.match(r'^[a-zA-Z0-9]+$', password):
        errors.append("Используйте только латинские символы и цифры.")
    if len(password) < 8:
        errors.append("Пароль слишком короткий! Минимум 8 символов.")
    if len(password) > 20:
        errors.append("Пароль слишком длинный! Максимум 20 символов.")
    if len(username) < 5:
        errors.append("Имя пользователя слишком короткое! Минимум 5 символов.")
    if len(username) > 20:
        errors.append("Имя пользователя слишком длинное! Максимум 20 символов.")
    if password != confirm_password:
        errors.append("Пароли не совпадают!")
    if not terms:
        errors.append("Примите политику приватности, чтобы продолжить!")
    
    if errors != []:
        return templates.TemplateResponse('auth/registration.html', {
            "request": request,
            "errors": errors,
            "user": None,
            "email": username,
            "password": password,
            "confirm_password": confirm_password,
        })
    
    password = pwd_context.hash(password)

    user = await User.create(
        username=username,
        hashed_password=password,
        disabled=False,
        is_admin=False,
        categories_rating={},
        avatar_link='imgs/user.svg',
        post_amount=0
    )

    if remember:
        access_token = manager.create_access_token(
            data={"sub": username},
            expires=timedelta(hours=48)
        )
    else:
        access_token = manager.create_access_token(
            data={"sub": username}
        )

    resp = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    manager.set_cookie(resp, access_token)

    return resp

@router_api.get("/logout")
async def logout(request: Request, user=Depends(manager)):
    response = templates.TemplateResponse("auth/login.html", {
        "request": request, 
        "user": None,
    })
    response.delete_cookie("BloGO-Auth")
    return response