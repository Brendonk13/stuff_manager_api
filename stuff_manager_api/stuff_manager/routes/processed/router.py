from ninja import Router
from stuff_manager.authentication.clerk import ClerkBearerAuth
# from .list_projects import list_projects, ListProjectsResponseSchema

processed_router = Router(auth=ClerkBearerAuth())

# ==================================== LISTS ====================================
# processed_router.add_api_operation(
#     "/projects",
#     ['GET'],
#     list_projects,
#     response=ListProjectsResponseSchema,
# )
