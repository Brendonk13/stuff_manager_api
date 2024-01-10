# from stuff_manager_api.stuff_manager.models import project
from ninja import Schema, Query
from stuff_manager.models import Action, Actions_Tags
from typing import Optional
from datetime import datetime
# from stuff_manager.schemas.action import ActionQueryFilterSchema, Actions_TagsQueryFilterSchema
from stuff_manager.schemas.action import ActionQueryFilterSchema

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
