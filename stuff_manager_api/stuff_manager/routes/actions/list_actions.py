# from stuff_manager_api.stuff_manager.models import project
from ninja import Schema, Query
# from asgiref.sync import sync_to_async
from stuff_manager.models import Action, Actions_Tags
from typing import Optional
from datetime import datetime
# from stuff_manager.schemas.action import ActionQueryFilterSchema, Actions_TagsQueryFilterSchema
from stuff_manager.schemas.action import ActionQueryFilterSchema, ActionDBSchema
# from stuff_manager.schemas.common import TagType

ListActionsResponseSchema = list[Optional[ActionDBSchema]]

def get_project_data(action):
    if not action.project_id:
        return { "project": None }

    return {
        "project": {
            "id": action.project_id,
            "name": action.project.name,
            "notes": action.project.notes,
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
            # todo: should I have ID's in here for the sake of type normalcy
            "tags": [
                {"value": tag.tag.value, "id": tag.tag.id}
                for tag
                in action.actions_tags_set.all()
            ],
            "required_context": [
                {"value": tag.tag.value, "id": tag.tag.id}
                for tag
                in action.actions_requiredcontexts_set.all()],
        }
        data.append(formatted_data)
    return data
