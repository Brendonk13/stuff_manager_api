# from stuff_manager_api.stuff_manager.models import project
from ninja import Schema
from stuff_manager.models import Action, Actions_Tags, Actions_Contexts, Project, Projects_User, Tag
from typing import Optional
from datetime import datetime
from stuff_manager.schemas.tag import NewTag as TagType
from stuff_manager.schemas.action import CreateActionSchema
from stuff_manager.schemas.project import ProjectDBSchema


# =================================== SCHEMA ===================================

class ProcessActionsRequestBody(Schema):
    unprocessed_id: int
    project: ProjectDBSchema
    actions: list[CreateActionSchema] # todo: NOT OPTIONAL

class CreateActionsResponseSchema(Schema):
    message: str


# =================================== TAGS =====================================
async def get_default_action_tags():
    # todo: cache these id's !!!!
    return {
        "delegated": await Tag.objects.aget(value="delegated"),
        "someday_maybe": await Tag.objects.aget(value="someday_maybe"),
        "cannot_be_done_yet": await Tag.objects.aget(value="cannot_be_done_yet"),
    }


def extract_tags_and_contexts(action_data):
    contexts = []
    default_tags = ["delegated", "someday_maybe", "cannot_be_done_yet"]
    tags = []
    # add default tags
    for tag in default_tags:
        if action_data.get(tag): # Ex.) if delegated==True, add delegated
            tags.append(tag)
        # delete from action_data which is used to create an action row
        if tag in action_data:
            del action_data[tag]

    # add custom tags
    if "tags" in action_data:
        tags += [tag["value"] for tag in action_data["tags"]]
        del action_data["tags"]

    if "contexts" in action_data:
        contexts += [context["value"] for context in action_data["contexts"]]
        del action_data["contexts"]

    return action_data, tags, contexts

async def add_tags_and_contexts(action_id: int, tags, contexts):
    # create Tags
    action_tags = []
    print("input tags")
    for tag in tags:
        if not tag:
            continue
        db_tag, _ = await Tag.objects.aget_or_create(value=tag)
        # print("created tag:", db_tag)
        action_tags.append(
            Actions_Tags(action_id=action_id, tag_id=db_tag.id)
        )

    print("going to create tags:", action_tags)
    await Actions_Tags.objects.abulk_create(action_tags)

    # create Contexts
    action_contexts = []
    for context in contexts:
        if not context:
            continue
        db_context, _ = await Tag.objects.aget_or_create(value=context)
        action_contexts.append(
            Actions_Contexts(action_id=action_id, tag_id=db_context.id)
        )

    await Actions_Contexts.objects.abulk_create(action_contexts)


# =================================== ENTRYPOINT ===============================

async def create_actions(request, data: ProcessActionsRequestBody):
    print("====================== create actions ======================")
    user = request.auth[0]
    project = data.project
    print("input project", project)
    if project.name and project.id == 0:
        project = await Project.objects.acreate(name=project.name, notes=project.notes)
        await Projects_User.objects.acreate(project_id=project.id, user_id=user.id)
        print(f"created project: {project}")

    # fine for now to do this in a for loop since currently you will not create that many all at once
    for action in data.actions:
        await create_action(project, action, user.id, data.unprocessed_id)
    return {
        "message": "Success",
        # "data": None,
    }


async def create_action(project, action, user_id: int, unprocessed_id: int):
    action_data, tags, contexts = extract_tags_and_contexts(action.dict())
    action_data["unprocessed_id"] = unprocessed_id

    if project.name:
        action_data = {**action_data, "project_id": project.id, "user_id": user_id}
    else:
        action_data = {**action_data, "user_id": user_id}

    print("action_data", action_data)
    new_action = await Action.objects.acreate(**action_data)
    print(f"created action: {new_action}")
    await add_tags_and_contexts(new_action.id, tags, contexts)
