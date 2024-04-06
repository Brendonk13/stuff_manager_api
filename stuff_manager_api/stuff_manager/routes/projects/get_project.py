# from stuff_manager_api.stuff_manager.models import project
# from ninja import Schema
from stuff_manager.models import Projects_User
from ninja.errors import HttpError
from stuff_manager.schemas.project import ProjectDBSchema

GetProjectResponseSchema = ProjectDBSchema

async def get_project(request, project_id: int):
    user = request.auth[0]
    try:
        project = await Projects_User.objects.select_related("project").aget(project_id=project_id)
        print("got project", project.project)

        if user.id != project.user_id:
            raise HttpError(403, "Unauthorized")

        return project.project

    except Projects_User.DoesNotExist:
        raise HttpError(404, "Project not found")
