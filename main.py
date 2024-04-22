import uvicorn

from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from tortoise.contrib.fastapi import register_tortoise

from api.auth import NotAuthenticatedException
from frontend_manager import router_api as frontend_routes
from api import router_api as backend_routes


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/node_modules", StaticFiles(directory="node_modules"), name="modules")

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=frontend_routes)
app.include_router(router=backend_routes)


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/errors/page_not_found")

@app.exception_handler(500)
async def internal_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/errors/internal_server_error")

@app.exception_handler(401)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url="/auth/login")

@app.exception_handler(405)
def auth_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse(url="/")


TORTOISE_ORM = {
    "connections": {
        "default": "mysql://root@localhost:3306/blogo",
    },
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "generate_schemas": True,
    "add_exception_handlers": True,
}

register_tortoise(app=app, config=TORTOISE_ORM)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        port=8001,
    )
