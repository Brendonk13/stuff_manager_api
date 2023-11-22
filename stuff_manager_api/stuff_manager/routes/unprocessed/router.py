from ninja import Router
from stuff_manager.authentication.clerk import ClerkBearerAuth
from .processActions import process_actions
from .unprocessed import create_unprocessed

unprocessed_router = Router(auth=ClerkBearerAuth())

unprocessed_router.add_api_operation("/actions", ['POST'], process_actions)
unprocessed_router.add_api_operation("", ['POST'], create_unprocessed)
