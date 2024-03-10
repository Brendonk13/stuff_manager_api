# from typing_extensions import TypedDict
from ninja import Schema

# todo: move this to its own file ?
# or make a file just for db schemas

# class NewTag(TypedDict):
# new tags are for when this is being created
class NewTag(Schema):
    value: str

class TagDBSchema(Schema):
    value: str
    id: int
