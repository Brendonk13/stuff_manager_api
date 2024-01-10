# from stuff_manager_api.stuff_manager.models import project
from ninja import Schema, Query
from stuff_manager.models import Action, Actions_Tags
from typing import Optional
from datetime import datetime
from stuff_manager.schemas.common import ActionQueryFilterSchema

class ActionDBSchema(Schema):
    title: str
    description: str
    created: datetime
    energy: Optional[int]
    project_id: Optional[int]
    # project_id: int # should I have this ????
    id: int

ListActionsResponseSchema = list[Optional[ActionDBSchema]]

# todo: cannot paginate async yet
# https://github.com/vitalik/django-ninja/pull/1030/commits
# @paginate
async def list_actions(request, filters: Query[ActionQueryFilterSchema]):
    user = request.auth[0]
    return [
        action
        async for action
        in filters.filter(Action.objects.filter(user_id=user.id)).distinct()
    ]


async def list_action_tags(queryset, user_id: int, filters: Query[ActionQueryFilterSchema]):
    return [
        action_tag.action
        async for action_tag
        in filters.filter(queryset.filter(action__user_id=user_id).select_related("action")).distinct()
    ]


# Endpoints for /delegated, /someday_maybe, etc
async def list_delegated(request, filters: Query[ActionQueryFilterSchema]):
    user = request.auth[0]
    return await list_action_tags(Actions_Tags.delegated, user.id, filters)

async def list_someday_maybe(request, filters: Query[ActionQueryFilterSchema]):
    user = request.auth[0]
    return await list_action_tags(Actions_Tags.someday_maybe, user.id, filters)

async def list_cannot_be_done_yet(request, filters: Query[ActionQueryFilterSchema]):
    user = request.auth[0]
    return await list_action_tags(Actions_Tags.cannot_be_done_yet, user.id, filters)
