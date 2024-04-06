from ninja import ModelSchema
# from typing import Optional
from stuff_manager.models import Project

# without the id
# class NewProjectDBSchema(Schema):
#     name: str
#     notes: str

class ProjectDBSchema(ModelSchema):
    class Meta:
        model = Project
        fields = "__all__"

# class ProjectDBSchema(Schema):
#     name: str
#     notes: Optional[str]
#     id: int
