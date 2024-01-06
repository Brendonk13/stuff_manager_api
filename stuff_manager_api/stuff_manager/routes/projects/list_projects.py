# from stuff_manager_api.stuff_manager.models import project
from ninja import Schema
from stuff_manager.models import Projects_User
from typing import List

class ProjectDBSchema(Schema):
    name: str
    notes: str
    id: int

class ListProjectsResponseSchema(Schema):
    message: str
    data: List[ProjectDBSchema]

async def projects_for_user(user_id: int):
    return [
        project.project
        async for project
        in Projects_User.objects.filter(user_id=user_id).select_related("project")
    ]


async def list_projects(request):
    user = request.auth[0]
    projects = await projects_for_user(user.id)
    print(f"projects for user: {projects}")
    return {
        "message": "Success",
        "data": projects,
    }
