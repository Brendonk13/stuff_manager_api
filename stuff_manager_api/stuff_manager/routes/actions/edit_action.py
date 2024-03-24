# from asgiref.sync import async_to_sync, sync_to_async
# from ninja import Schema
from ninja.errors import HttpError
from typing import Optional
from django.forms.models import model_to_dict

from stuff_manager.models import Action, Tag, Actions_Tags, Actions_RequiredContexts, Project
from stuff_manager.schemas.action import EditActionBody, ActionDBSchema
from stuff_manager.schemas.tag import NewTag

EditActionResponseSchema = Optional[ActionDBSchema]

async def delete_tags(action_id: int, tags: list[NewTag]):
    original_tag_ids = set([
        tag.tag
        async for tag
        in Actions_Tags.objects.filter(action_id=action_id).select_related("tag")
    ])
    # original_tag_ids = set(tag.id for tag in original_tags)
    new_tag_ids = set(tag.id for tag in tags)
    deleted_tags = original_tag_ids - new_tag_ids
    print("original_tag_ids", original_tag_ids)
    print("new_tag_ids", new_tag_ids)
    print("deleted_tags", deleted_tags)
    for tag_id in deleted_tags:
        print("deleting tag with id: ", tag_id)
        await Actions_Tags.objects.filter(action_id=action_id, tag_id=tag_id).adelete()

async def create_new_tags(action_id: int, tags: list[NewTag]):
    action_tags = []
    for tag in tags:
        if "id" in tag.keys():
            continue
        db_tag, _ = await Tag.objects.acreate(value=tag.value)
        # print("created tag:", db_tag)
        action_tags.append(
            Actions_Tags(action_id=action_id, tag_id=db_tag.id)
        )

    print("going to create tags:", action_tags)
    await Actions_Tags.objects.abulk_create(action_tags)

async def delete_contexts(action_id: int, contexts: list[NewTag]):
    original_context_ids = set([
        context.tag.id
        async for context
        in Actions_RequiredContexts.objects.filter(action_id=action_id).select_related("tag")
    ])
    # original_context_ids = set(context.id for context in original_contexts)
    new_context_ids = set(context.id for context in contexts)
    deleted_contexts = original_context_ids - new_context_ids
    print("original_context_ids", original_context_ids)
    print("new_context_ids", new_context_ids)
    print("deleted_contexts", deleted_contexts)
    for context_id in deleted_contexts:
        print("deleting context with id: ", context_id)
        await Actions_RequiredContexts.objects.filter(action_id=action_id, tag_id=context_id).adelete()


async def create_new_contexts(action_id: int, contexts: list[NewTag]):
    action_contexts = []
    for context in contexts:
        if "id" in context.keys():
            continue
        db_context, _ = await Tag.objects.acreate(value=context.value)
        # print("created context:", db_context)
        action_contexts.append(
            Actions_RequiredContexts(action_id=action_id, tag_id=db_context.id)
        )

    print("going to create contexts:", action_contexts)
    await Actions_RequiredContexts.objects.abulk_create(action_contexts)


# could not get the stuff in "extract_action_data" to work async
async def edit_action(request, action_id: int, data: EditActionBody):
    user = request.auth[0]
    try:
        action = await Action.objects.aget(id=action_id)
        if action.user_id != user.id:
            return 403, { "message": "Unauthorized", "data": None }

    except Action.DoesNotExist:
        raise HttpError(404, "Action not found")

    for attr, value in data.dict().items():
        if value is None:
            continue
        if attr == "project":
            value = value.id
            attr = "project_id"
        print("attr", attr)

        if attr == "tags":
            # print("doing tags", value)
            # if len(value):
            print("doing tags")
            await create_new_tags(action_id, value)
            await delete_tags(action_id, value)
        elif attr == "required_context":
            # if len(value):
            await create_new_contexts(action_id, value)
            await delete_contexts(action_id, value)
        else:
            setattr(action, attr, value)



    await action.asave()
    print("DICT", model_to_dict(action))
    action_dict = model_to_dict(action)
    del action_dict["unprocessed"]
    del action_dict["user"]
    # del action_dict["project"]
    # required_context = [{"value": context.tag.value, "id": context.tag.id} async for context in Actions_RequiredContexts.objects.filter(action_id=action_id).select_related("tag")]
    # tags = [{"value": tag.tag.value, "id": tag.tag.id} async for tag in Actions_Tags.objects.filter(action_id=action_id).select_related("tag")]
    # print("tags", tags, type(tags))
    # print("contexts", required_context, type(required_context))
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
        "created": action.created, # for some reason this doesnt come from model_to_dict
    }
