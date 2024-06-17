from fastapi import APIRouter
from .auth import router_api as auth_router_api
from .user import router_api as user_router_api
from .post import router_api as post_router_api
from .admin import router_api as admin_router_api


router_api = APIRouter()

router_api.include_router(router=auth_router_api)
router_api.include_router(router=user_router_api)
router_api.include_router(router=post_router_api)
router_api.include_router(router=admin_router_api)
