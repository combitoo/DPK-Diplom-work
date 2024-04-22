from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from api.auth import manager


router_api = APIRouter(prefix="/info", tags=["Info"])
templates = Jinja2Templates(directory="templates")


@router_api.get('/about_product', response_class=HTMLResponse)
async def info_about_product(request: Request, user=Depends(manager.optional)):
    return templates.TemplateResponse("info/about_product.html", {
        "request": request,
        "user": user,
    })

@router_api.get('/privacy_policy', response_class=HTMLResponse)
async def info_policy_privacy(request: Request, user=Depends(manager.optional)):
    return templates.TemplateResponse("info/policy_privacy.html", {
        "request": request,
        "user": user,
    })

@router_api.get('/contact', response_class=HTMLResponse)
async def info_product(request: Request, user=Depends(manager.optional)):
    return templates.TemplateResponse("info/contact.html", {
        "request": request,
        "user": user,
    })
