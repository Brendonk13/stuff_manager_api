# from typing_extensions import TypedDict
from ninja import Schema
from typing import Optional

# class NewTag(TypedDict):
# new tags are for when this is being created
class NewTag(Schema):
    value: str
    # this is optional cuz we may send a list of new Tags with no id, and existing Tags which have an id
    id: Optional[int] = None

class TagDBSchema(Schema):
    value: str
    id: int
