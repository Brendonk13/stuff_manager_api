from ninja import Router
from stuff_manager.authentication.clerk import ClerkBearerAuth
from .create_actions import create_actions_view, CreateActionsResponseSchema

actions_router = Router(auth=ClerkBearerAuth())

# ==================================== LISTS ====================================
actions_router.add_api_operation(
    "",
    ['POST'],
    create_actions_view,
    response=CreateActionsResponseSchema,
)
