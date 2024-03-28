from ninja.errors import HttpError
# from django.forms.models import model_to_dict

from stuff_manager.models import Completion_Notes, Action
from stuff_manager.schemas.action import ActionCompletedSchema

GetActionCompletionResponseSchema = ActionCompletedSchema


# could not get the stuff in "extract_action_data" to work async
# fine since its only one get request
async def get_action_completion(request, action_id: int):
    user = request.auth[0]
    try:
        action = await Action.objects.aget(id=action_id)
        if action.user_id != user.id:
            return 403, { "message": "Unauthorized", "data": None }
        completion_notes = await Completion_Notes.objects.aget(action_id=action_id)
    except Action.DoesNotExist or Completion_Notes.DoesNotExist:
        raise HttpError(404, "Action or completion_notes not found")

    return completion_notes
