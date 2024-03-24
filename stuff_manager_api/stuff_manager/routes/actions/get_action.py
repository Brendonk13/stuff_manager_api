# from asgiref.sync import async_to_sync, sync_to_async
# from ninja import Schema
from ninja.errors import HttpError
from typing import Optional

from stuff_manager.models import Action
from stuff_manager.schemas.action import ActionDBSchema
from .utils.extract_action_data import extract_action_data


GetActionResponseSchema = Optional[ActionDBSchema]


# could not get the stuff in "extract_action_data" to work async
# fine since its only one get request
def get_action(request, action_id: int):
    user = request.auth[0]
    formatted_action = {}
    try:
        action = Action.objects.filter(id=action_id).prefetch_related("actions_tags_set", "actions_requiredcontexts_set").first()
        # for action in Action.objects.filter(id=action_id).prefetch_related("actions_tags_set", "actions_requiredcontexts_set"):
        if action.user_id != user.id:
            return 403, { "message": "Unauthorized", "data": None }
        if action is None:
            raise HttpError(404, "Action not found")
    except Action.DoesNotExist:
        raise HttpError(404, "Action not found")

    formatted_action = extract_action_data(action)
    # await add_tags_and_contexts_to_response(action)
    # print("returned getAction:", formatted_action)

    return formatted_action
