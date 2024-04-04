from ninja.errors import HttpError
from stuff_manager.models import Action


async def get_action_or_404(action_id: int, user_id: int, get_project=False):
    try:
        select_related = ["completion_notes"]
        if get_project:
            select_related.append("project")
        action = await Action.objects.select_related(*select_related).aget(id=action_id)

        if action.user_id != user_id:
            raise HttpError(403, "Unauthorized")
    except Action.DoesNotExist:
        raise HttpError(404, "Action not found")

    return action
