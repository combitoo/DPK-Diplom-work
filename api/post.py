from fastapi import APIRouter, Depends, Form, UploadFile, status
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from .auth import manager
from database.models import User, Post, Comment, Category
from frontend_manager.utils.seconds_to_time import Converter
import math

import os
import shutil
import random


router_api = APIRouter(prefix="/post", tags=["Post"])
templates = Jinja2Templates(directory="templates")


@router_api.post("/create")
async def post_create(
    title: str = Form(""),
    text: str = Form(""),
    preview_link: UploadFile = None,
    categories: list = Form([]),
    user=Depends(manager)
):
    errors = []

    if len(title) < 3:
        errors.append("Заголовок не может быть менее 3 символов!")
    if len(title) > 128:
        errors.append("Заголовок не может быть более 128 символов!")
    if len(text) < 10:
        errors.append("Текст не может быть менее 10 символов!")
    if len(text) > 10240:
        errors.append("Текст со всем форматированием не может быть более 10240 символов!")
    if categories[0] == 'undefined':
        errors.append("Выберите хотя бы 1 категорию!")
    if len(categories[0].split(',')) > 3:
        errors.append("Максимум 3 категории!")

    if errors != []:
        return JSONResponse(
            status_code=400,
            content={
            "errors_descs": errors,
        })
    
    post = await Post.create(
        title=title,
        text=text,
        created_by_id=user.id,
        post_rating=0,
        preview_link="",
        time_to_read=Converter().seconds_to(math.floor(len(text) / 20))
    )

    existing_categories = await Category.filter(id__in=categories[0].split(","))
    if len(existing_categories) != len(categories[0].split(",")):
        return JSONResponse(
            status_code=400,
            content={"errors_descs": ["Одна или несколько категорий не найдены."]},
        )
    for category in existing_categories:
        category.post_amount += 1
        await category.save()
    await post.categories.add(*existing_categories)

    user = await User.get(id=user.id)
    user.post_amount += 1
    await user.save()

    if preview_link is not None and len(preview_link.filename) != 0:
        upload_dir = os.path.join(os.getcwd(), "static/imgs/posts/")

        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        dest = os.path.join(upload_dir, f"{post.id}.png")

        with open(dest, "wb") as buffer:
            shutil.copyfileobj(preview_link.file, buffer)
        
        post.preview_link = f"/imgs/posts/{post.id}.png?{random.randint(1, 2e9)}"
        await post.save()
    
    return RedirectResponse("/user/profile", status_code=status.HTTP_302_FOUND)


@router_api.post("/delete")
async def post_delete(
    request: Request,
    post_id: int = Form(0),
    user=Depends(manager)
):
    post = await Post.get_or_none(id=post_id).prefetch_related("categories")

    if post is not None and post.created_by_id == user.id:
        for category in post.categories:
            category.post_amount -= 1
            await category.save()
        await post.delete()

    user = await User.get(id=user.id)
    user.post_amount -= 1
    await user.save()

    return RedirectResponse("/user/profile", status_code=status.HTTP_302_FOUND)


@router_api.post("/create_comment")
async def post_create_comment(
    request: Request, 
    post_id: int = Form(0),
    comment: str = Form(""),
    user=Depends(manager)
):
    if len(comment) > 256:
        return RedirectResponse(str(request.headers.get("Referer")), status_code=status.HTTP_302_FOUND)
    if len(comment) < 5:
        return RedirectResponse(str(request.headers.get("Referer")), status_code=status.HTTP_302_FOUND)
    
    comment = await Comment.create(
        text=comment,
        created_by_id=user.id,
        post_id=post_id,
    )

    return RedirectResponse(str(request.headers.get("Referer")), status_code=status.HTTP_302_FOUND)


@router_api.post("/delete_comment")
async def post_delete_comment(
    request: Request,
    comment_id: int = Form(0),
    user=Depends(manager)
):
    comment = await Comment.get_or_none(id=comment_id)

    if comment is not None and comment.created_by_id == user.id:
        await comment.delete()

    return RedirectResponse(str(request.headers.get("Referer")), status_code=status.HTTP_302_FOUND)