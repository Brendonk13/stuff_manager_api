from typing import Optional
from ninja import Schema
from stuff_manager.models import Projects_User
from ninja.errors import HttpError
from stuff_manager.schemas.project import ProjectDBSchema

class EditProjectBody(Schema):
    id: int
    name: Optional[str]
    notes: Optional[str]

class EditProjectResponseSchema(Schema):
    message: str
    data: ProjectDBSchema

async def edit_project(request, project_id: int, data: EditProjectBody):
    user = request.auth[0]
    try:
        project = await Projects_User.objects.select_related("project").aget(project_id=project_id)
        print("got project", project.project)

        if user.id != project.user_id:
            return 403, { "message": "Unauthorized", "data": None }

        for attr, value in data.dict().items():
            setattr(project.project, attr, value)
        await project.project.asave()

        return {
            "message": "Success",
            "data": project.project,
        }
    except Projects_User.DoesNotExist:
        raise HttpError(404, "Project not found")
