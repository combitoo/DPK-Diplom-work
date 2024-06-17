from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from api.auth import manager
from database.models import Post, User, Comment, Category
from .utils.seconds_to_time import Converter
import math


router_api = APIRouter(prefix="/categories", tags=["Categories"])
templates = Jinja2Templates(directory="templates")


@router_api.get('/', response_class=HTMLResponse)
async def category_index(request: Request, user=Depends(manager.optional)):
    category = await Category.all().prefetch_related("posts")
    return templates.TemplateResponse("categories/index.html", {
        "request": request,
        "user": user,
        "categories": category,
    })


@router_api.get('/{category_id}', response_class=HTMLResponse)
async def category_about(request: Request, category_id: int, user=Depends(manager.optional)):
    categories = await Category.all()
    category = await Category.get(id=category_id)
    posts = await Post.filter(categories=category_id).all().prefetch_related("created_by", "categories")
    
    if len(posts) < 1:
        posts = "404"
    
    return templates.TemplateResponse("categories/about.html", {
        "request": request,
        "user": user,
        "categories": categories,
        "category": category,
        "posts": posts,
    })