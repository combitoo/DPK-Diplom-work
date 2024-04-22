from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from api.auth import manager


router_api = APIRouter(prefix="/auth", tags=["Auth"])
templates = Jinja2Templates(directory="templates")


@router_api.get('/login', response_class=HTMLResponse)
async def auth_login(request: Request, user=Depends(manager.optional)):
    return templates.TemplateResponse("auth/login.html", {
        "request": request,
        "user": user,
    })


@router_api.get('/registration', response_class=HTMLResponse)
async def auth_registration(request: Request, user=Depends(manager.optional)):
    return templates.TemplateResponse("auth/registration.html", {
        "request": request,
        "user": user,
    })