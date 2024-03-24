from django.db.models import Q
from ninja import FilterSchema, Schema
from typing import Optional
from datetime import datetime
from .project import  ProjectDBSchema
# from stuff_manager.schemas.tag import NewTag as TagType, TagDBSchema
from stuff_manager.schemas.tag import NewTag, TagDBSchema

# NOte: wont this fail with empty list of tags ??
class CreateActionSchema(Schema):
    title              : str
    description        : str
    date               : Optional[datetime] = None
    energy             : Optional[int]
    cannot_be_done_yet : bool = False
    delegated          : bool = False
    someday_maybe      : bool = False
    tags               : list[NewTag]
    required_context   : list[NewTag]


# NOte: wont this fail with empty list of tags ??
# making fields not required with Optional is not sufficient for pydantic: https://github.com/pydantic/pydantic/issues/6463#issuecomment-1622517803
class EditActionBody(Schema):
    id               : int
    title            : Optional[str] = None
    description      : Optional[str] = None
    energy           : Optional[int] = None
    date             : Optional[datetime] = None
    project          : Optional[ProjectDBSchema] = None
    required_context : Optional[list[NewTag]] = None
    tags             : Optional[list[NewTag]] = None


class ActionDBSchema(Schema):
    id               : int
    title            : str
    description      : str
    created          : datetime
    energy           : Optional[int]
    date             : Optional[datetime] # todo: added this later instead of at start by accident, should work
    project          : Optional[ProjectDBSchema]
    required_context : Optional[list[TagDBSchema]]
    tags             : Optional[list[TagDBSchema]] # todo: return tag ID's as well


# https://django-ninja.dev/guides/input/filtering/
class ActionQueryFilterSchema(FilterSchema):
    title            : Optional[str]       = None
    project_id       : Optional[int]       = None
    energy           : Optional[int]       = None
    date             : Optional[datetime]  = None
    tags             : Optional[list[str]] = None
    required_context : Optional[list[str]] = None

    # Format for query string: {hostname}/api/actions?tags=["delegated"]&required_context=["newContext"]&title=another all lists3


    def filter_tags(self, _tags: Optional[list[str]]) -> Q:
        if not _tags:
            return Q()
        # parse query string
        tags = [tag.strip("\"'") for tag in _tags[0].rstrip("]").lstrip("[").split(",")]
        return Q(actions_tags__tag__value__in=tags)

    def filter_required_context(self, _tags: Optional[list[str]]) -> Q:

        if not _tags:
            return Q()
        # parse query string
        tags = [tag.strip("\"'") for tag in _tags[0].rstrip("]").lstrip("[").split(",")]
        return Q(actions_requiredcontexts__tag__value__in=tags)
