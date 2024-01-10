from ninja import Router
from stuff_manager.authentication.clerk import ClerkBearerAuth
from .create_actions import create_actions, CreateActionsResponseSchema
# from .list_actions import list_actions, list_delegated, list_someday_maybe, list_cannot_be_done_yet, ListActionsResponseSchema
from .list_actions import list_actions, ListActionsResponseSchema

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

# todo: change the response schema ???
# actions_router.add_api_operation(
#     "/delegated",
#     ['GET'],
#     list_delegated,
#     response=ListActionsResponseSchema,
# )

# actions_router.add_api_operation(
#     "/someday_maybe",
#     ['GET'],
#     list_someday_maybe,
#     response=ListActionsResponseSchema,
# )

# actions_router.add_api_operation(
#     "/cannot_be_done_yet",
#     ['GET'],
#     list_cannot_be_done_yet,
#     response=ListActionsResponseSchema,
# )
