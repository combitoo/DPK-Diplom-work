from fastapi import APIRouter, Depends, status, Form, File, UploadFile
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi_login.exceptions import InvalidCredentialsException 

from typing import Optional, Union, Annotated
from passlib.context import CryptContext
from datetime import timedelta

from database.models import User
from api.auth import manager

import os
import shutil
import random
import re


router_api = APIRouter(prefix="/user", tags=["User"])
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router_api.post('/settings_creds')
async def user_settings(
    request: Request,
    username: str = Form(""),
    password: str = Form(None),
    user = Depends(manager),
):
    errors = []
    
    if not re.match(r'^[a-zA-Z0-9]+$', username) or not re.match(r'^[a-zA-Z0-9]+$', password):
        errors.append("Используйте только латинские символы и цифры.")
    if password is not None and len(password) < 8:
        errors.append("Пароль слишком короткий! Минимум 8 символов.")
    if password is not None and len(password) > 20:
        errors.append("Пароль слишком длинный! Максимум 20 символов.")
    if len(username) < 5:
        errors.append("Имя пользователя слишком короткое! Минимум 5 символов.")
    if len(username) > 20:
        errors.append("Имя пользователя слишком длинное! Максимум 20 символов.")
    
    if errors != []:
        return templates.TemplateResponse('user/settings.html', {
            "request": request,
            "errors_creds": errors,
            "user": user,
        })
    
    my_user = await User.get(id=user.id)

    if username != my_user.username:
        my_user.username = username

    if password is not None and not pwd_context.verify(password, my_user.hashed_password):
        my_user.hashed_password = pwd_context.hash(password)
    
    await my_user.save()

    access_token = manager.create_access_token(
        data={"sub": my_user.username},
        expires=timedelta(hours=48)
    )
    
    resp = RedirectResponse(url="/user/settings", status_code=status.HTTP_303_SEE_OTHER)
    manager.set_cookie(resp, access_token)

    return resp


@router_api.post('/settings_descs')
async def user_settings(
    description: str = Form(""),
    avatar_image: UploadFile = None,
    user = Depends(manager),
):
    errors = []

    if len(description) < 5:
        errors.append("Описание профиля слишком короткое! Минимум 5 символов.")
    if len(description) > 511:
        errors.append("Описание профиля слишком длинное! Максимум 511 символов.")
    
    if errors != []:
        return JSONResponse(
            status_code=400,
            content={
            "errors_descs": errors,
        })
    
    my_user = await User.get(id=user.id)

    if avatar_image is not None and len(avatar_image.filename) != 0:
        upload_dir = os.path.join(os.getcwd(), "static/imgs/users/")

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        dest = os.path.join(upload_dir, f"{user.id}.png")

        with open(dest, "wb") as buffer:
            shutil.copyfileobj(avatar_image.file, buffer)
        
        my_user.avatar_link = f"/imgs/users/{user.id}.png?{random.randint(1, 2e9)}"
    
    if description != my_user.description:
        my_user.description = description
    
    await my_user.save()

    return RedirectResponse(url="/user/profile", status_code=303)