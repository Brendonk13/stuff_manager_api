from ninja import Schema
from ninja.errors import HttpError
from typing import Optional

from stuff_manager.models import Action, Actions_Tags
from stuff_manager.schemas.action import ActionDBSchema


GetActionResponseSchema = Optional[ActionDBSchema]

async def get_action(request, action_id: int):
    user = request.auth[0]
    try:
        action = await Action.objects.filter(id=action_id).prefetch_related("actions_tags_set", "actions_requiredcontexts_set").select_related("project").first()
        if action is None:
            raise HttpError(404, "Action not found")
    except Action.DoesNotExist:
        raise HttpError(404, "Action not found")

    if action.user_id != user.id:
        return 403, { "message": "Unauthorized", "data": None }

    action["tags"] = [
        { "value": tag.tag.value, "id": tag.tag.id, }
        for tag
        in action.actions_tags_set.all()
    ]
    action["required_context"] = [
        { "value": tag.tag.value, "id": tag.tag.id, }
        for tag
        in action.actions_requiredcontexts_set.all()
    ]


    return action

