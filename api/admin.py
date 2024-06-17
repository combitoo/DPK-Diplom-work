from fastapi import APIRouter, Depends, status, Form, File, UploadFile
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi_login.exceptions import InvalidCredentialsException 

from typing import Optional, Union, Annotated
from passlib.context import CryptContext
from datetime import timedelta

from database.models import User, Post, Comment
from api.auth import manager

import re


router_api = APIRouter(prefix="/admin", tags=["Admin"])
templates = Jinja2Templates(directory="templates")


@router_api.post('/user/update/{user_id}')
async def update_user_by_admin(
    request: Request,
    user_id: int,
    login: str = Form(""),
    role: str = Form(""),
    description: str = Form(""),
    user = Depends(manager),
):
    if user.role != "admin":
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    errors = []
    
    if not re.match(r'^[a-zA-Z0-9]+$', login) or not re.match(r'^[a-zA-Z0-9]+$', role):
        errors.append("Используйте только латинские символы и цифры.")
    if len(login) < 5:
        errors.append("Имя пользователя слишком короткое! Минимум 5 символов.")
    if len(login) > 20:
        errors.append("Имя пользователя слишком длинное! Максимум 20 символов.")
    if len(description) < 5:
        errors.append("Описание профиля слишком короткое! Минимум 5 символов.")
    if len(description) > 511:
        errors.append("Описание профиля слишком длинное! Максимум 511 символов.")
    
    if errors != []:
        return templates.TemplateResponse('admin/index.html', {
            "request": request,
            "errors": errors,
            "user": user,
        })
    
    other_user = await User.get_or_none(id=user_id)

    if other_user is None:
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    
    other_user.username = login
    other_user.role = role
    other_user.description = description

    await other_user.save()

    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)


@router_api.get('/user/delete/{user_id}')
async def delete_user_by_admin(
    request: Request,
    user_id: int,
    user = Depends(manager),
):
    if user.role != "admin":
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    other_user = await User.get_or_none(id=user_id)

    if other_user is None:
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

    user = await User.get(id=user.id)
    user.post_amount -= 1
    await user.save()
    await other_user.delete()

    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)


@router_api.post('/post/update/{post_id}')
async def update_post_by_admin(
    request: Request,
    post_id: int,
    title: str = Form(""),
    text: str = Form(""),
    user = Depends(manager),
):
    if user.role != "admin":
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    errors = []
    
    if len(title) < 5:
        errors.append("Поле заголовок слишком короткое! Минимум 5 символов.")
    if len(title) > 128:
        errors.append("Поле заголовок слишком длинное! Максимум 128 символов.")
    if len(text) < 5:
        errors.append("Поле текст слишком короткое! Минимум 5 символов.")
    if len(text) > 10240:
        errors.append("Поле текст слишком длинное! Максимум 1019 символов.")
    
    if errors != []:
        return templates.TemplateResponse('admin/index.html', {
            "request": request,
            "errors": errors,
            "user": user,
        })
    
    other_post = await Post.get_or_none(id=post_id)

    if other_post is None:
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    
    other_post.title = title
    other_post.text = text

    await other_post.save()

    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)


@router_api.get('/post/delete/{post_id}')
async def delete_post_by_admin(
    request: Request,
    post_id: int,
    user = Depends(manager),
):
    if user.role != "admin":
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    
    other_post = await Post.get_or_none(id=post_id).prefetch_related("created_by")

    if other_post is None:
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

    await other_post.delete()

    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)