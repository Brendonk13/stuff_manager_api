# from stuff_manager_api.stuff_manager.models import project
from ninja import Schema
from stuff_manager.models import Projects_User
from typing import List
from ninja.errors import HttpError

class ProjectDBSchema(Schema):
    name: str
    notes: str
    id: int

class GetProjectResponseSchema(Schema):
    message: str
    data: ProjectDBSchema


async def get_project(request, project_id: int):
    user = request.auth[0]
    try:
        # todo: test ownership 403 response
        project = await Projects_User.objects.select_related("project").aget(project_id=project_id)
        print("got project", project.project)

        if user.id != project.user_id:
            return 403, { "message": "Unauthorized", "data": None }
        return {
            "message": "Success",
            "data": project.project,
        }
    except Projects_User.DoesNotExist:
        raise HttpError(404, "Project not found")
