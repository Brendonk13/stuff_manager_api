from ninja import Router
from stuff_manager.authentication.clerk import ClerkBearerAuth
from .list_projects import list_projects, ListProjectsResponseSchema

projects_router = Router(auth=ClerkBearerAuth())

# ==================================== LISTS ====================================
projects_router.add_api_operation(
    "",
    ['GET'],
    list_projects,
    response=ListProjectsResponseSchema,
)
