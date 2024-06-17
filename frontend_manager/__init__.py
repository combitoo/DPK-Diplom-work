from fastapi import APIRouter
from .info import router_api as info_router_api
from .main_page import router_api as main_router_api
from .auth import router_api as auth_router_api
from .error_404 import router_api as error_router_api
from .user import router_api as user_router_api
from .post import router_api as post_router_api
from .categories import router_api as categories_router_api
from .admin import router_api as admin_router_api


router_api = APIRouter()

router_api.include_router(router=info_router_api)
router_api.include_router(router=main_router_api)
router_api.include_router(router=auth_router_api)
router_api.include_router(router=error_router_api)
router_api.include_router(router=user_router_api)
router_api.include_router(router=post_router_api)
router_api.include_router(router=categories_router_api)
router_api.include_router(router=admin_router_api)
