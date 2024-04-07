# from asgiref.sync import async_to_sync, sync_to_async
# from ninja import Schema
from ninja.errors import HttpError
from typing import Optional, Union
from django.forms.models import model_to_dict
# from typing_extensions import TypedDict
from ninja import Schema
from datetime import datetime
from pytz import UTC

from stuff_manager.schemas.tag import TagDBSchema
from stuff_manager.utils.get_action_or_404 import get_action_or_404
from stuff_manager.models import Action, Tag, Actions_Tags, Actions_RequiredContexts, Project
# from stuff_manager.schemas.action import EditActionBody, ActionDBSchema, ActionCompletedSchema
from stuff_manager.schemas.action import ActionDBSchema
from stuff_manager.schemas.project import ProjectDBSchema
from stuff_manager.schemas.tag import NewTag

EditActionResponseSchema = Optional[ActionDBSchema]

class SentinelValueClass(Schema):
    pass

SentinelValue = SentinelValueClass()
# tbh the best is to just never send null, but what about the project

# class EditActionBody(ModelSchema):
class EditActionBody(Schema):
    required_context : Union[Optional[list[TagDBSchema]] , SentinelValueClass] = SentinelValue
    tags             : Union[Optional[list[TagDBSchema]] , SentinelValueClass] = SentinelValue
    title            : Union[Optional[str]               , SentinelValueClass] = SentinelValue
    description      : Union[Optional[str]               , SentinelValueClass] = SentinelValue
    project          : Union[Optional[ProjectDBSchema]   , SentinelValueClass] = SentinelValue
    completed        : Union[Optional[bool]              , SentinelValueClass] = SentinelValue
    deleted          : Union[Optional[bool]              , SentinelValueClass] = SentinelValue
    date             : Union[Optional[datetime]          , SentinelValueClass] = SentinelValue
    energy           : Union[Optional[int]               , SentinelValueClass] = SentinelValue
    deleted_date     : Union[Optional[datetime]          , SentinelValueClass] = SentinelValue




async def delete_tags(action_id: int, tags: Optional[list[NewTag]]):
    if tags is None:
        return
    original_tag_ids = set([
        tag.tag.id
        async for tag
        in Actions_Tags.objects.filter(action_id=action_id).select_related("tag")
    ])
    new_tag_ids = set(tag.id for tag in tags)
    deleted_tags = original_tag_ids - new_tag_ids
    # print("original_tag_ids", original_tag_ids)
    # print("new_tag_ids", new_tag_ids)
    # print("deleted_tags", deleted_tags)
    for tag_id in deleted_tags:
        print("deleting tag with id: ", tag_id)
        await Actions_Tags.objects.filter(action_id=action_id, tag_id=tag_id).adelete()

async def create_new_tags(action_id: int, tags: Optional[list[NewTag]]):
    if tags is None:
        return
    action_tags = []
    for tag in tags:
        if hasattr(tag, "id"):
            if await Actions_Tags.objects.filter(action_id=action_id, tag_id=tag.id).aexists():
                continue
            db_tag = await Tag.objects.aget(id=tag.id)
        else:
            db_tag, _ = await Tag.objects.acreate(value=tag.value)
        # print("created tag:", db_tag)
        action_tags.append(
            Actions_Tags(action_id=action_id, tag_id=db_tag.id)
        )

    print("going to create tags:", action_tags)
    t = await Actions_Tags.objects.abulk_create(action_tags)
    print("created tags", t)

async def delete_contexts(action_id: int, contexts: Optional[list[NewTag]]):
    if contexts is None:
        return
    original_context_ids = set([
        context.tag.id
        async for context
        in Actions_RequiredContexts.objects.filter(action_id=action_id).select_related("tag")
    ])
    new_context_ids = set(context.id for context in contexts)
    deleted_contexts = original_context_ids - new_context_ids
    # print("original_context_ids", original_context_ids)
    # print("new_context_ids", new_context_ids)
    # print("deleted_contexts", deleted_contexts)
    for context_id in deleted_contexts:
        print("deleting context with id: ", context_id)
        await Actions_RequiredContexts.objects.filter(action_id=action_id, tag_id=context_id).adelete()


async def create_new_contexts(action_id: int, contexts: Optional[list[NewTag]]):
    if contexts is None:
        return
    action_contexts = []
    for context in contexts:
        if hasattr(context, "id"):
            # continue if we already have this association
            if await Actions_RequiredContexts.objects.filter(action_id=action_id, tag_id=context.id).aexists():
                continue
            db_context = await Tag.objects.aget(id=context.id)
        else:
            db_context, _ = await Tag.objects.acreate(value=context.value)
        # print("created context:", db_context)
        action_contexts.append(
            Actions_RequiredContexts(action_id=action_id, tag_id=db_context.id)
        )

    print("going to create contexts:", action_contexts)
    await Actions_RequiredContexts.objects.abulk_create(action_contexts)



async def save_action(action, action_id: int, data: EditActionBody):
    for attr, value in data.dict().items():
        if (
            attr == "completed_date" # make sure this value doesnt overwrite completed
            or attr == "deleted_date" # make sure this value doesnt overwrite completed
            or value == SentinelValue
            or isinstance(getattr(data, attr), SentinelValueClass)
        ):
            continue

       # must transform project to project_id for getattr to succeed
        if attr == "project":
            value = value["id"] if value is not None else None
            attr = "project_id"

        # this will reset the unprocessed id if its not passed
        if attr == "unprocessed":
            attr = "unprocessed_id"

        #when deleted, it reset completed
        # print("attr", attr, "value", value)

        if value is None and hasattr(action, attr) and getattr(action, attr) is None:
            print("original is none and so is the new")
            continue

        if attr == "tags":
            await create_new_tags(action_id, data.tags)
            await delete_tags(action_id, data.tags)
        elif attr == "required_context":
            await create_new_contexts(action_id, data.required_context)
            await delete_contexts(action_id, data.required_context)
        elif attr == "deleted":
            if data.deleted:
                print("setting deleted to now")
                setattr(action, "deleted_date", datetime.now(tz=UTC))
            elif data.deleted == False:
                print("setting deleted to None")
                setattr(action, "deleted_date", None)
        elif attr == "completed":
            # if action.completed_date is None and data.completed:
            if data.completed:
                print("setting complete to now")
                setattr(action, "completed_date", datetime.now(tz=UTC))
            elif data.completed == False:
                print("setting complete to incomplete")
                setattr(action, "completed_date", None)
        else:
            print(f"SETATTR, attr: {attr}, value: {value}")
            setattr(action, attr, value)

    return await action.asave()

async def format_response(action_id: int, action):
    action_dict = model_to_dict(action)
    del action_dict["unprocessed"]
    del action_dict["user"]
    del action_dict["project"]
    return {
        **action_dict,
        "tags": [
            {"value": tag.tag.value, "id": tag.tag.id}
            async for tag
            in Actions_Tags.objects.filter(action_id=action_id).select_related("tag")
        ],
        "required_context": [
            {"value": context.tag.value, "id": context.tag.id}
            async for context
            in Actions_RequiredContexts.objects.filter(action_id=action_id).select_related("tag")
        ],
        "user_id": action.user_id,
        "unprocessed_id": action.unprocessed_id,
        # dont get from database if this action has no project
        "project": await Project.objects.aget(id=action.project_id) if action.project_id is not None else None,
        "created": action.created, # for some reason this doesnt come from model_to_dict
    }

async def edit_action(request, action_id: int, data: EditActionBody):
    user = request.auth[0]
    action = await get_action_or_404(action_id=action_id, user_id=user.id)

    print("data ==", data)
    await save_action(action, action_id, data)
    print('saved action', action)

    # construct response
    return await format_response(action_id, action)
