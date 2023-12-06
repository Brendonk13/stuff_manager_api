# from stuff_manager_api.stuff_manager.models import project
from ninja import Schema
from stuff_manager.models import Action, Actions_Tags, Actions_RequiredContexts, Project
from typing import List, Optional
from datetime import datetime

class ActionSchema(Schema):
    title: str
    description: str
    date: Optional[datetime] = None
    energy: Optional[int]

class ProjectSchema(Schema):
    name: str
    notes: str
    id: int # if this is zero then we need to create a new project

class ProcessActions(Schema):
    unprocessed_id: int
    project: ProjectSchema
    steps: List[ActionSchema] # todo: NOT OPTIONAL

    # @staticmethod
    # def resolve_user_id(obj, context):
    #     user = context['request'].auth[0]
    #     return user.id

    @staticmethod
    def resolve_unprocessed_id(obj): # change from camel case
        return obj['unprocessedId']



class CreateActionsResponseSchema(Schema):
    message: str
    # data: List[ProjectDBSchema]

# def create_actions(request):
#     return

async def create_actions_view(request, data: ProcessActions):
    print("====================== create actions ======================")
    user = request.auth[0]
    project = data.project
    print("input project", project)
    if project.name and project.id == 0:
        project = await Project.objects.acreate(name=project.name, notes=project.notes)
        print(f"created project: {project}")
    # for action in data.actions:
    for action in data.steps:
        if project.name:
            action_data = {**action.dict(), "project_id": project.id, "user_id": user.id}
        else:
            action_data = {**action.dict(), "user_id": user.id}
        new_action = await Action.objects.acreate(**action_data)
        print(f"created action: {new_action}")

    return {
        "message": "Success",
        # "data": None,
    }


# async def process_actions(request, data: ProcessActions):
#     # todo: add error handling
#     user = request.auth[0]
#     print(user)
#     the_data = data.dict()
#     is_project = len(the_data['steps']) > 1
#     project = await Project.objects.acreate(**{"name": the_data['title']}) if is_project else None
#     print(the_data)
#     for action in the_data['steps']:
#         if is_project:
#             action_data = {**action, "project": project, "user": user}
#         else:
#             action_data = {**action, "user": user}
#         print(f"about to create action: {action_data}")
#         created = await Action.objects.acreate(**action_data)
#         print(f"created: {created}")
#     return {"message": "Success", }

