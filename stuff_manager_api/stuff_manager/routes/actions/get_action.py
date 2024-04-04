# from asgiref.sync import async_to_sync, sync_to_async
# from ninja import Schema
from ninja.errors import HttpError
from typing import Optional
from django.forms.models import model_to_dict

from stuff_manager.models import Action
from stuff_manager.schemas.action import ActionDBSchema
from .utils.extract_action_data import extract_action_data
from stuff_manager.utils.get_action_or_404 import get_action_or_404

GetActionResponseSchema = ActionDBSchema

# could not get the stuff in "extract_action_data" to work async
# fine since its only one get request
async def get_action(request, action_id: int):
    user = request.auth[0]
    return await extract_action_data(
        await get_action_or_404(action_id=action_id, user_id=user.id, get_project=True)
    )
