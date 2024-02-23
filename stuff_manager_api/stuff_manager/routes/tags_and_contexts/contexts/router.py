from ninja import Router
from stuff_manager.authentication.clerk import ClerkBearerAuth
from .list_contexts import list_contexts, ListContextsResponse

contexts_router = Router(auth=ClerkBearerAuth())


# ==================================== LISTS ====================================
contexts_router.add_api_operation(
    "",
    ['GET'],
    list_contexts,
    response=ListContextsResponse,
)
