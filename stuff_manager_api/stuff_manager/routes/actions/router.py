from ninja import Router
from stuff_manager.authentication.clerk import ClerkBearerAuth
from .create_actions import create_actions, CreateActionsResponseSchema
# from .list_actions import list_actions, list_delegated, list_someday_maybe, list_cannot_be_done_yet, ListActionsResponseSchema
from .list_actions import list_actions, ListActionsResponseSchema
from .get_action import get_action, GetActionResponseSchema
from .edit_action import edit_action, EditActionResponseSchema

actions_router = Router(auth=ClerkBearerAuth())

# ==================================== POSTS ====================================
actions_router.add_api_operation(
    "",
    ['POST'],
    create_actions,
    response=CreateActionsResponseSchema,
)

# ==================================== LISTS ====================================
actions_router.add_api_operation(
    "",
    ['GET'],
    list_actions,
    response=ListActionsResponseSchema,
)

# ==================================== GETS =====================================
actions_router.add_api_operation(
    "/{action_id}",
    ['GET'],
    get_action,
    response=GetActionResponseSchema,
)

# ==================================== PUTS =====================================
actions_router.add_api_operation(
    "/{action_id}",
    ['PUT'],
    edit_action,
    response=EditActionResponseSchema,
)

