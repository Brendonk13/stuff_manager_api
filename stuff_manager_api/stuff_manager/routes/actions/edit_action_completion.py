from typing import Optional
# from ninja.errors import HttpError
from stuff_manager.models import Completion_Notes, Action
from stuff_manager.schemas.action import ActionCompletedSchema
from stuff_manager.utils.get_action_or_404 import get_action_or_404
from django.forms.models import model_to_dict

EditCompletionNotesResponse = Optional[ActionCompletedSchema]

async def edit_completion_notes(action, completion_data: ActionCompletedSchema):
    has_completed_attr = hasattr(completion_data, "completed")
    if has_completed_attr:
        # print("hascompleted")
        # add this for the action.asave() later
        action.completed = completion_data.completed
        delattr(completion_data, "completed") # so we can convert the rest of the data to a dict

    # if hasattr(completion_data, "id") and completion_data.id is None:
    # prevent this from being in the **completion_data.dict()
    # if hasattr(completion_data, "id"):
    #     delattr(completion_data, "id")

    print(action, type(action), model_to_dict(action))
    # TODO: test this by deleting the action's id field to null
    # print("getattr", getattr(action, "id"))
    # if getattr(action, "completion_notes", None):
    # print(hasattr(action, "completion_notes"), action.completion_notes.id)
    if hasattr(action, "completion_notes") and action.completion_notes.action_id:
        print("has id", completion_data.dict())
        # queryset = Completion_Notes.objects.filter(id=action.completion_notes_id)
        queryset = Completion_Notes.objects.filter(action_id=action.completion_notes.action_id)
        await queryset.aupdate(**completion_data.dict())
        action_completion = await queryset.afirst()
    else:
        print("create  new actioncompletion", completion_data.dict())
        action_completion = await Completion_Notes.objects.acreate(**completion_data.dict())

    print(action_completion)
    # save changes
    if hasattr(action, "completion_notes") and action.completion_notes.action_id != action_completion.action_id:
        action.completion_notes.action_id = action_completion.action_id
        await action.asave()
        print("DICT", model_to_dict(action))
    elif has_completed_attr:
        await action.asave()
        print("DICT", model_to_dict(action))

    print("DICT", model_to_dict(action_completion))
    return action_completion


async def edit_action_completion(request, action_id: int, data: ActionCompletedSchema):
    user = request.auth[0]
    action = await get_action_or_404(action_id, user.id)
    print("DICT", model_to_dict(action))

    return await edit_completion_notes(action, data)
