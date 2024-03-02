from ninja import Schema

class ProjectDBSchema(Schema):
    name: str
    notes: str
    id: int

