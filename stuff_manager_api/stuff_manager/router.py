from ninja import Router
# from .authentication.clerk import ClerkBearerAuth
from .routes.tests.router import test_router
from .routes.unprocessed.router import unprocessed_router
from .routes.processed.router import processed_router
from .routes.projects.router import projects_router
from .routes.actions.router import actions_router

# api_router = Router(auth=ClerkBearerAuth())
# auth is handled by different routers
api_router = Router()

api_router.add_router("/tests", test_router)
api_router.add_router("/unprocessed", unprocessed_router)
api_router.add_router("/processed", processed_router)
api_router.add_router("/projects", projects_router)
api_router.add_router("/actions", actions_router)
