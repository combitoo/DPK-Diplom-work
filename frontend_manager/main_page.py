from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

from api.auth import manager
from database.models import Post
from frontend_manager.utils.pagination import get_pagintaion_page
from settings import LIMIT_POST

import math


router_api = APIRouter(tags=["Main page"])
templates = Jinja2Templates(directory="templates")


@router_api.get('/', response_class=HTMLResponse)
async def main(request: Request, offset: int = 0, user=Depends(manager.optional)):
    pages_amount = math.ceil(len(await Post.all()) / LIMIT_POST)

    # if offset < 0 or offset * LIMIT_POST > pages_amount + 1:
    #     return RedirectResponse("/")
    
    pagination_html = await get_pagintaion_page(limit=LIMIT_POST, offset=offset, pages_amount=pages_amount)
    posts = await Post.all().offset(offset * LIMIT_POST).limit(LIMIT_POST).order_by("-created_at").prefetch_related("created_by")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user,
        "posts": posts,
        "pagination_html": pagination_html,
    })
