from ninja import Schema
from typing import Optional

# without the id
# class NewProjectDBSchema(Schema):
#     name: str
#     notes: str

class ProjectDBSchema(Schema):
    name: str
    notes: Optional[str]
    id: int
