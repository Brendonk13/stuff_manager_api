from ninja import Router
from stuff_manager.authentication.clerk import ClerkBearerAuth
from .list_projects import list_projects, ListProjectsResponseSchema
from .get_project import get_project, GetProjectResponseSchema

projects_router = Router(auth=ClerkBearerAuth())

# ==================================== LIST ====================================
projects_router.add_api_operation(
    "",
    ['GET'],
    list_projects,
    response=ListProjectsResponseSchema,
)

# ==================================== GET =====================================
projects_router.add_api_operation(
    "/{project_id}",
    ['GET'],
    get_project,
    response=GetProjectResponseSchema,
)
