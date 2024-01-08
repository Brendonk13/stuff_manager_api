# from stuff_manager_api.stuff_manager.models import project
from ninja import Schema
from stuff_manager.models import Action, Actions_Tags
from typing import List, Optional
from datetime import datetime

class ActionDBSchema(Schema):
    title: str
    description: str
    created: datetime
    energy: Optional[int]
    project_id: Optional[int]
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


# todo: make this work by user id, not action id
async def list_delegated(request):
    user = request.auth[0]
    actions = [delegated.action async for delegated in Actions_Tags.delegated.filter(action__user_id=user.id).select_related("action")]
    return {
        "message": "Success",
        "data": actions,
    }

async def list_someday_maybe(request):
    user = request.auth[0]
    actions = [someday_maybe.action async for someday_maybe in Actions_Tags.someday_maybe.filter(action__user_id=user.id).select_related("action")]
    return {
        "message": "Success",
        "data": actions,
    }

async def list_cannot_be_done_yet(request):
    user = request.auth[0]
    actions = [cannot_be_done.action async for cannot_be_done in Actions_Tags.cannot_be_done.filter(action__user_id=user.id).select_related("action")]
    return {
        "message": "Success",
        "data": actions,
    }

