# from stuff_manager_api.stuff_manager.models import project
from asgiref.sync import sync_to_async, async_to_sync
from ninja import Schema, Query
# from asgiref.sync import sync_to_async
from stuff_manager.models import Action, Actions_Tags
from typing import Optional
from datetime import datetime
# from stuff_manager.schemas.action import ActionQueryFilterSchema, Actions_TagsQueryFilterSchema
from stuff_manager.schemas.action import ActionQueryFilterSchema
from stuff_manager.schemas.common import TagType



# choices are using Actions (with reverse foreign key), Actions_Tags with non-working stuff.., or actions with raw sql query ...
# todo: try actions_tags again but make the validator by action__actions_tags__tag__value__in=tags




class ActionDBSchema(Schema):
    id: int
    title: str
    description: str
    created: datetime
    energy: Optional[int]
    project_id: Optional[int]
    tags: Optional[list[str]]
    required_context: Optional[list[str]]

ListActionsResponseSchema = list[Optional[ActionDBSchema]]

# todo: cannot paginate async yet
# https://github.com/vitalik/django-ninja/pull/1030/commits
# @paginate
def list_actions(request, query_filters: Query[ActionQueryFilterSchema]):
    user = request.auth[0]
    data = []
    for action in query_filters.filter(Action.objects.filter(user_id=user.id).prefetch_related("actions_tags_set", "actions_requiredcontexts_set")).distinct():
        formatted_data = {
            "id": action.id,
            "title": action.title,
            "description": action.description,
            "energy": action.energy,
            "project_id": action.project_id,
            "created": action.created,
            "tags": [thing.tag.value for thing in action.actions_tags_set.all()],
            "required_context": [thing.tag.value for thing in action.actions_requiredcontexts_set.all()],
        }
        data.append(formatted_data)

    return data
