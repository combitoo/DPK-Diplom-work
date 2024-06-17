from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from api.auth import manager
from database.models import Post, User, Comment, Category
from .utils.seconds_to_time import Converter
import math


router_api = APIRouter(prefix="/post", tags=["Post"])
templates = Jinja2Templates(directory="templates")


@router_api.get('/create', response_class=HTMLResponse)
async def post_create(request: Request, user=Depends(manager)):
    categories = await Category.all()
    return templates.TemplateResponse("post/create.html", {
        "request": request,
        "user": user,
        "categories": categories,
    })


@router_api.get('/read', response_class=HTMLResponse)
async def post_create(request: Request, post_id: int = 0, user=Depends(manager.optional)):
    post = await Post.get_or_none(id=int(post_id)).prefetch_related("created_by", "categories")
    comments = await Comment.filter(post_id=post_id).all().order_by("-created_at").prefetch_related("created_by")
    if post is None:
        post = "404"
    else:
        converter = Converter()
        post.time_amount = converter.seconds_to(math.floor(len(post.text) / 20))

    return templates.TemplateResponse("post/read.html", {
        "request": request,
        "user": user,
        "post": post,
        "comments": comments,
    })
