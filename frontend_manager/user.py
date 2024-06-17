from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from api.auth import manager
from database.models import Post, User
from frontend_manager.utils.pagination import get_pagintaion_page
from settings import LIMIT_USER

import math


router_api = APIRouter(prefix="/user", tags=["User"])
templates = Jinja2Templates(directory="templates")


@router_api.get('/', response_class=HTMLResponse)
async def user_settings(request: Request, offset: int = 0, user=Depends(manager.optional)):
    pages_amount = math.ceil(len(await User.all()) / LIMIT_USER)

    # if offset < 0 or offset * LIMIT_USER > pages_amount + 1:
    #     return RedirectResponse("/user")
    
    pagination_html = await get_pagintaion_page(limit=LIMIT_USER, offset=offset, pages_amount=pages_amount, type_for="/user")
    users = await User.all().offset(offset * LIMIT_USER).limit(LIMIT_USER).only("username", "avatar_link", "id", "description", "role")

    return templates.TemplateResponse("user/index.html", {
        "request": request,
        "user": user,
        "users": users,
        "pagination_html": pagination_html
    })


@router_api.get('/settings', response_class=HTMLResponse)
async def user_settings(request: Request, user=Depends(manager)):
    return templates.TemplateResponse("user/settings.html", {
        "request": request,
        "user": user,
    })


@router_api.get('/profile', response_class=HTMLResponse)
async def user_profile(request: Request, user=Depends(manager)):
    posts = await Post.all().filter(created_by=user.id).prefetch_related('categories').order_by("-created_at")

    if len(posts) < 1:
        posts = "404"

    return templates.TemplateResponse("user/profile.html", {
        "request": request,
        "user": user,
        "posts": posts,
    })


@router_api.get('/profile/{username}', response_class=HTMLResponse)
async def user_profile(request: Request, username: str = "", user=Depends(manager.optional)):
    another_user = await User.get_or_none(username=username)

    if another_user is None:
        return RedirectResponse("/user")

    if user is not None and another_user.id == user.id:
        return RedirectResponse("/user/profile")
    
    posts = await Post.all().filter(created_by=another_user.id).prefetch_related("created_by", "categories")

    if len(posts) < 1:
        posts = "404"

    return templates.TemplateResponse("user/profile_another.html", {
        "request": request,
        "user": user,
        "another_user": another_user,
        "posts": posts,
    })