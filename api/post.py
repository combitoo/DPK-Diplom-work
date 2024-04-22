from fastapi import APIRouter, Depends, Form, UploadFile, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from .auth import manager
from database.models import User, Post, Comment
from frontend_manager.utils.seconds_to_time import Converter
import math

import os
import shutil
import random


router_api = APIRouter(prefix="/post", tags=["Post"])
templates = Jinja2Templates(directory="templates")


@router_api.post("/create")
async def post_create(
    request: Request, 
    title: str = Form(""),
    text: str = Form(""),
    preview_link: UploadFile = None,
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

    if errors != []:
        return templates.TemplateResponse('post/create.html', {
            "request": request,
            "errors_descs": errors,
            "user": user,
            "input": {
                "title": title,
                "text": text,
            }
        })
    
    post = await Post.create(
        title=title,
        text=text,
        created_by_id=user.id,
        post_rating=0,
        preview_link="",
        time_to_read=Converter().seconds_to(math.floor(len(text) / 20))
    )

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
    post = await Post.get_or_none(id=post_id)

    if post is not None and post.created_by_id == user.id:
        await post.delete()

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