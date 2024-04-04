# from stuff_manager_api.stuff_manager.models import project
from ninja import Query
# from asgiref.sync import sync_to_async
from stuff_manager.models import Action
from typing import Optional
from ninja import ModelSchema
# from datetime import datetime
# from stuff_manager.schemas.action import ActionQueryFilterSchema, Actions_TagsQueryFilterSchema
from stuff_manager.schemas.action import ActionQueryFilterSchema, ActionDBSchema
# from stuff_manager.schemas.common import TagType
from .utils.extract_action_data import extract_action_data


ListActionsResponseSchema = list[Optional[ActionDBSchema]]


# todo: be able to search by regex in descriptions

# todo: cannot paginate async yet
# https://github.com/vitalik/django-ninja/pull/1030/commits
# @paginate
async def list_actions(request, query_filters: Query[ActionQueryFilterSchema]):
    user = request.auth[0]
    data = [
        # todo: make this function async by getting tags in seperate queries
        await extract_action_data(action)
        async for action
        in query_filters.filter(
            Action.objects.filter(user_id=user.id).select_related("project", "completion_notes")
        ).distinct()
    ]
    # todo: should the select related be outside of query_filters.filter ?
    print("all actions", data)
    return data
