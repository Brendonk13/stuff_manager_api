# from asgiref.sync import async_to_sync, sync_to_async
# from ninja import Schema
from ninja.errors import HttpError
from typing import Optional
from django.forms.models import model_to_dict
from typing_extensions import TypedDict

from stuff_manager.models import Action, Tag, Actions_Tags, Actions_RequiredContexts, Project
from stuff_manager.schemas.action import EditActionBody, ActionDBSchema, ActionCompletedSchema
from stuff_manager.schemas.tag import NewTag

EditActionResponseSchema = Optional[ActionDBSchema]

async def delete_tags(action_id: int, tags: Optional[list[NewTag]]):
    if tags is None:
        return
    original_tag_ids = set([
        tag.tag.id
        async for tag
        in Actions_Tags.objects.filter(action_id=action_id).select_related("tag")
    ])
    # original_tag_ids = set(tag.id for tag in original_tags)
    # new_tag_ids = set(tag["id"] for tag in tags)
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
        # if "id" in tag.keys():
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
    # new_context_ids = set(context["id"] for context in contexts)
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
        # if "id" in context.keys():
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


# async def edit_completion_notes(action_id: int, completion_notes: ActionCompletedSchema):
#     return



# could not get the stuff in "extract_action_data" to work async
async def edit_action(request, action_id: int, data: EditActionBody):
    user = request.auth[0]
    try:
        action = await Action.objects.aget(id=action_id)
        if action.user_id != user.id:
            return 403, { "message": "Unauthorized", "data": None }

    except Action.DoesNotExist:
        raise HttpError(404, "Action not found")

    # how to deal with completed ? -- similar to tags
    # get current completion status and new status
    # if was completed and now not completed, then keep the completion notes, but change completed boolean field
    # if was not completed and now completed, mark the chang
    # if completion notes changed, mark the change
    # -- no deletes necessary

    # print("OG DICT", model_to_dict(action))
    # print()
    print("data", data)

    # print("all data", data.dict())
    # print()
    for attr, value in data.dict().items():
        # must transform project to project_id for getattr to succeed
        if attr == "project":
            # print("proj", value)
            value = value["id"] if value is not None else None
            attr = "project_id"

        if value is None and getattr(action, attr) is None:
            print("original is none and so is the new")
            continue

        if attr == "tags":
            # await create_new_tags(action_id, value)
            await create_new_tags(action_id, data.tags)
            await delete_tags(action_id, data.tags)
        elif attr == "required_context":
            await create_new_contexts(action_id, data.required_context)
            await delete_contexts(action_id, data.required_context)
        # elif attr == "completion_notes":
        #     await edit_completion_notes(aciton_id, value)
        else:
            setattr(action, attr, value)



    await action.asave()
    print("DICT", model_to_dict(action))
    action_dict = model_to_dict(action)
    del action_dict["unprocessed"]
    del action_dict["user"]
    del action_dict["project"]
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

        # dont get from database if this action has no project
        "project": await Project.objects.aget(id=action.project_id) if data.dict()["project"] is not None else None,
        "created": action.created, # for some reason this doesnt come from model_to_dict
    }
