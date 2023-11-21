from ninja import Router
from .auth import test_auth_router

test_router = Router()

test_router.add_router("/auth", test_auth_router)
