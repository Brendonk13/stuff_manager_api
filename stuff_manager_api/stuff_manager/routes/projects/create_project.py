from typing import Optional
from ninja import Schema
from stuff_manager.models import Projects_User, Project
from stuff_manager.schemas.project import ProjectDBSchema

class CreateProjectBody(Schema):
    id: int
    name: Optional[str]
    notes: Optional[str]

class CreateProjectResponseSchema(Schema):
    data: ProjectDBSchema

async def create_project(request, data: CreateProjectBody):
    user = request.auth[0]
    project = await Project.objects.acreate(name=data.name, notes=data.notes)
    await Projects_User.objects.acreate(project_id=project.id, user_id=user.id)
    print(f"created project: {project}")

    return {
        "data": project,
    }
