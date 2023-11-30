from ninja import Router
from stuff_manager.authentication.clerk import ClerkBearerAuth
from .process_actions import process_actions
from .create_unprocessed import create_unprocessed, CreateUnprocessedResponseSchema
from .get_unprocessed import get_unprocessed, GetUnprocessedResponseSchema

unprocessed_router = Router(auth=ClerkBearerAuth())

# ==================================== POSTS ====================================
unprocessed_router.add_api_operation(
    "/actions",
    ['POST'],
    process_actions,
)

unprocessed_router.add_api_operation(
    "",
    ['POST'],
    create_unprocessed,
    response=CreateUnprocessedResponseSchema
)


# ==================================== GETS ====================================
# @api.get("/items/{item_id}")
unprocessed_router.add_api_operation(
    "/{unprocessed_id}",
    ['GET'],
    get_unprocessed,
    response=GetUnprocessedResponseSchema,
)
