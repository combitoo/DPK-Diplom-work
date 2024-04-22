from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from api.auth import manager


router_api = APIRouter(prefix="/errors", tags=["Info"])
templates = Jinja2Templates(directory="templates")


@router_api.get('/page_not_found', response_class=HTMLResponse)
async def errors_page_not_found(request: Request, user=Depends(manager.optional)):
    return templates.TemplateResponse("errors/404.html", {
        "request": request,
        "user": user,
    })


@router_api.get('/internal_server_error', response_class=HTMLResponse)
async def errors_page_not_found(request: Request, user=Depends(manager.optional)):
    return templates.TemplateResponse("errors/500.html", {
        "request": request,
        "user": user,
    })