from ninja.errors import HttpError
from stuff_manager.models import Action


async def get_action_or_404(action_id: int, user_id: int):
    try:
        action = await Action.objects.select_related("completion_notes").aget(id=action_id)

        if action.user_id != user_id:
            raise HttpError(403, "Unauthorized")
    except Action.DoesNotExist:
        raise HttpError(404, "Action not found")

    return action
