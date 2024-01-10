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
def list_actions(request, filters: Query[ActionQueryFilterSchema]):
    user = request.auth[0]
    # data = [
    #     action_tag
    #     async for action_tag
    #     # in filters.filter(Actions_Tags.objects.filter(action__user_id=user.id).select_related("action", "tag")).distinct()
    #     # in filters.filter(Actions_Tags.objects.filter(action__user_id=user.id).select_related("action")).distinct()
    #     in filters.filter(Action.objects.filter(user_id=user.id).prefetch_related("actions_tags_set")).distinct()
    # ]

    data = []
    # async for action in filters.filter(Action.objects.filter(user_id=user.id).prefetch_related("actions_tags_set", "actions_requiredcontexts_set")).distinct():
    # async for action in filters.filter(Action.objects.filter(user_id=user.id).prefetch_related("actions_tags_set", "actions_requiredcontexts_set")).distinct():
    # async for action in filters.filter(Action.objects.filter(user_id=user.id)).distinct().aiterator():
    for action in filters.filter(Action.objects.filter(user_id=user.id).prefetch_related("actions_tags_set", "actions_requiredcontexts_set")).distinct():
        # print("type", type(action))
        # action.tags = [action.tag.value async for action in action.actions_tags_set.all()]
        # action.tags = action.actions_tags_set.only("tag__value").all()

        # tags = [i.tag_id for i in action.actions_tags_set.all()]
        # print("tags", tags)

        # action.tags = sync_to_async.actions_tags_set.all()
        # action.tags = []
        # for tag in action.actions_tags_set.all():
            # print("tag", tag)
            # action.tags.append(tag.tag.value)
        used = {
            "id": action.id,
            "title": action.title,
            "description": action.description,
            "energy": action.energy,
            "project_id": action.project_id,
            "created": action.created,
            # "tags": tags,
            # "tags": [thing.tag async for thing in await sync_to_async(action.actions_tags_set.only("tag__value").all)()],
            # "tags": [thing async for thing in await sync_to_async(action.actions_tags_set.all)()],
            # "tags": [thing.tag async for thing in action.actions_tags_set.all()],
            # "tags": [thing.tag async for thing in action.actions_tags_set.all()],
            "tags": [thing.tag.value for thing in action.actions_tags_set.all()],
            "required_context": [thing.tag.value for thing in action.actions_requiredcontexts_set.all()],
        }
        data.append(used)


    # print("data", data)
    return data


# async def list_action_tags(queryset, user_id: int, filters: Query[Actions_TagsQueryFilterSchema]):
#     return [
#         action_tag.action
#         async for action_tag
#         in filters.filter(queryset.filter(action__user_id=user_id).select_related("action")).distinct()
#         # in filters.filter(queryset.filter(action__user_id=user_id).select_related("action", "tag")).distinct()
#     ]


