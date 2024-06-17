from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from api.auth import manager
from database.models import Post, User, Comment, Category
from .utils.seconds_to_time import Converter
import math


router_api = APIRouter(prefix="/admin", tags=["Admin"])
templates = Jinja2Templates(directory="templates")


@router_api.get('/', response_class=HTMLResponse)
async def category_index(request: Request, user=Depends(manager)):
    if user.role != "admin":
        return RedirectResponse("/")
    
    users = await User.all()
    posts = await Post.all().prefetch_related("categories", "created_by")
    comments = await Comment.all().prefetch_related("created_by", "post")
    
    return templates.TemplateResponse("admin/index.html", {
        "request": request,
        "user": user,
        "users": users,
        "posts": posts,
        "comments": comments,
    })