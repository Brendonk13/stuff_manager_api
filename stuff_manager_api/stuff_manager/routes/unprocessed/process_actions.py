from stuff_manager.models.project import Project
from ninja import Schema
from datetime import datetime

import json
from ninja import ModelSchema
from stuff_manager.models import Action
from typing import Optional

class ActionSchema(Schema):
    name: str
    description: str
    date: Optional[datetime] = None


# todo: change the shape of this data -- project should be its own thing
class ProcessActions(Schema):
    name: str
    description: str
    # project: bool # WAS HERER
    steps: list[ActionSchema] #NOTE: think this got changed to "actions"
    # user: int # WAS HERER

    # @staticmethod
    # def resolve_project(obj, context):
    #     body = json.loads(context["request"].body)
    #     return len(body['steps']) > 1

    # @staticmethod
    # def resolve_user(obj, context):
    #     user = context['request'].auth[0]
    #     return user.id





async def process_actions(request, data: ProcessActions):
    # todo: add error handling
    # todo: change logic for project -- just create one if the data was passed
    # dont I also need to check if this is an existing project ?????
    user = request.auth[0]
    print(user)
    the_data = data.dict()
    is_project = len(the_data['steps']) > 1

    # wait, I dont think this is being used at all !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # todo: change from title ==> project_name
    # todo: this should be adding them to Projects_User table also !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # project = await Project.objects.acreate(**{"name": the_data['title']}) if is_project else None
    project = await Project.objects.acreate(**{"name": the_data['name']}) if is_project else None
    print(the_data)
    for action in the_data['steps']:
        if is_project:
            action_data = {**action, "project": project, "user": user}
        else:
            action_data = {**action, "user": user}
        print(f"about to create action: {action_data}")
        created = await Action.objects.acreate(**action_data)
        print(f"created: {created}")
    return {"message": "Success", }
