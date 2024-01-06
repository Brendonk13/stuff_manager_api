from ninja import Router
from stuff_manager.authentication.clerk import ClerkBearerAuth
from .create_actions import create_actions_view, CreateActionsResponseSchema
from .list_actions import list_actions, ListActionsResponseSchema

actions_router = Router(auth=ClerkBearerAuth())

# ==================================== POSTS ====================================
actions_router.add_api_operation(
    "",
    ['POST'],
    create_actions_view,
    response=CreateActionsResponseSchema,
)

# ==================================== LISTS ====================================
actions_router.add_api_operation(
    "",
    ['GET'],
    list_actions,
    response=ListActionsResponseSchema,
)
