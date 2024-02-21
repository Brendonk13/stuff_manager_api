# from stuff_manager_api.stuff_manager.models import project
from asgiref.sync import sync_to_async, async_to_sync
from ninja import Schema, Query
# from asgiref.sync import sync_to_async
from stuff_manager.models import Action, Actions_Tags
from typing import Optional
from datetime import datetime
# from stuff_manager.schemas.action import ActionQueryFilterSchema, Actions_TagsQueryFilterSchema
from stuff_manager.schemas.action import ActionQueryFilterSchema
# from stuff_manager.schemas.common import TagType

class ProjectSchema(Schema):
    project_id: int
    name: str

class ActionDBSchema(Schema):
    id: int
    title: str
    description: str
    created: datetime
    energy: Optional[int]
    # todo: maybe return the project title as well
    # project_id: Optional[int]
    project: Optional[ProjectSchema]
    tags: Optional[list[str]]
    required_context: Optional[list[str]]

ListActionsResponseSchema = list[Optional[ActionDBSchema]]

def get_project_data(action):
    if not action.project_id:
        return {"project": None}

    return {
        "project": {
            "project_id": action.project_id,
            "name": action.project.name,
        }
    }


# todo: cannot paginate async yet
# https://github.com/vitalik/django-ninja/pull/1030/commits
# @paginate
def list_actions(request, query_filters: Query[ActionQueryFilterSchema]):
    user = request.auth[0]
    data = []
    # todo: should the seelect related be outside of query_filters.filter ?
    for action in query_filters.filter(
        Action.objects.filter(user_id=user.id).prefetch_related("actions_tags_set", "actions_requiredcontexts_set").select_related("project")
    ).distinct():
        formatted_data = {
            "id": action.id,
            "title": action.title,
            "description": action.description,
            "energy": action.energy,
            # "project_id": action.project_id,
            **get_project_data(action),
            "created": action.created,
            "tags": [thing.tag.value for thing in action.actions_tags_set.all()],
            "required_context": [thing.tag.value for thing in action.actions_requiredcontexts_set.all()],
        }
        data.append(formatted_data)
    return data
