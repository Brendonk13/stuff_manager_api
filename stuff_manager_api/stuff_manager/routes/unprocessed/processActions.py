from stuff_manager.models.project import Project
from ninja import Schema
from datetime import datetime

from ninja import ModelSchema
from stuff_manager.models import Action
from typing import List, Optional

class ActionSchema(Schema):
    # class Meta:
    #     model = Action
    # fields = ['title', 'description', 'date', 'user']
    title: str
    description: str
    date: Optional[datetime] = None

    @staticmethod
    def resolve_user(obj, context):
        request = context["request"]
        print("in child schema")
        print(f"context: {context}")
        print(f"context : {dir(context)}")

        # print(f"context request: {request}")
        # print(f"context request: {dir(request)}")
        user = request.auth[0]
        return user.id

class ProcessActions(Schema):
    title: str
    description: str
    project: bool
    steps: List[ActionSchema]
    user: int

    @staticmethod
    def resolve_project(obj, context):
        print(f"context: {context}")
        request = context["request"]
        # print(f"request : {request}")
        print(f"request body: {dir(request)}")
        print(f"request body scheme: {request.scheme}")
        print(f"request body scheme: {dir(request.scheme)}")
        user = request.auth[0]
        user_id = user.id
        context["user_id"] = user_id
        print(f"user: User({user}, {user_id}")
        return True

    @staticmethod
    def resolve_user(obj, context):
        user = context['request'].auth[0]
        return user.id





async def process_actions(request, data: ProcessActions):
    # todo: make this async
    user = request.auth[0]
    print(user)
    the_data = data.dict()
    is_project = len(the_data['steps']) > 1
    project = Project.objects.acreate(**{"name": the_data.title}) if is_project else None
    print(the_data)
    for action in the_data['steps']:
        if is_project:
            action_data = {**action, "project": project, "user": user}
        else:
            action_data = {**action, "user": user}
        print(f"about to create action: {action_data}")
        created = await Action.objects.acreate(**action_data)
        print(f"created: {created}")
    return
    # user = User(username=data.username) # User is django auth.User
    # user.set_password(data.password)
    # user.save()
    # # ... return ?
