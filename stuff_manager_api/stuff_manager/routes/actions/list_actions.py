# from stuff_manager_api.stuff_manager.models import project
from ninja import Schema
from stuff_manager.models import Action
from typing import List
from datetime import datetime

class ActionDBSchema(Schema):
    title: str
    description: str
    created: datetime
    energy: int
    project_id: int
    # project_id: int # should I have this ????
    id: int

class ListActionsResponseSchema(Schema):
    message: str
    data: List[ActionDBSchema]

async def actions_for_user(user_id: int):
    return [
        action
        async for action
        in Action.objects.filter(user_id=user_id)
    ]


async def list_actions(request):
    user = request.auth[0]
    actions = await actions_for_user(user.id)
    print(f"actions for user: {actions}")
    return {
        "message": "Success",
        "data": actions,
    }
