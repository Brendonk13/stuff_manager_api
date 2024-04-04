from django.db.models import Q
from ninja import FilterSchema, Schema, ModelSchema
from typing import Optional
from datetime import datetime
from .project import ProjectDBSchema
from stuff_manager.models import Action
# from stuff_manager.schemas.tag import NewTag as TagType, TagDBSchema
from stuff_manager.schemas.tag import NewTag, TagDBSchema

class ActionCompletedSchema(Schema):
    action_id  : int
    start_time : Optional[datetime] = None
    end_time   : Optional[datetime] = None
    duration   : Optional[list[int]] = None
    notes      : Optional[str]      = ""
    # completed_date  : Optional[bool]     = None

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
# todo: make some of these not optional
class EditActionBody(Schema):
    id               : int
    title            : Optional[str] = None
    description      : Optional[str] = None
    energy           : Optional[int] = None
    date             : Optional[datetime] = None
    project          : Optional[ProjectDBSchema] = None
    required_context : Optional[list[NewTag]] = None
    tags             : Optional[list[NewTag]] = None
    completed_date   : Optional[datetime] = None
    deleted_date     : Optional[datetime] = None
    # completion_notes : Optional[ActionCompletedSchema] = None
    # the notes are in a seperate endpoint

class ActionDBSchema(ModelSchema):
    # this value is computed from completed_date
    completed        : Optional[bool] = None
    completion_notes : Optional[ActionCompletedSchema] = None
    project          : Optional[ProjectDBSchema]
    required_context : Optional[list[TagDBSchema]]
    tags             : Optional[list[TagDBSchema]] # todo: return tag ID's as well
    # deleted_date     : Optional[datetime] = None

    class Meta:
        model = Action
        # fields = ['id', 'title', 'description', 'last_name']
        fields = "__all__"


# class ActionDBSchema(Schema):
#     id               : int
#     title            : str
#     description      : str
#     created          : datetime
#     energy           : Optional[int]
#     date             : Optional[datetime] # todo: added this later instead of at start by accident, should work
#     project          : Optional[ProjectDBSchema]
#     required_context : Optional[list[TagDBSchema]]
#     tags             : Optional[list[TagDBSchema]] # todo: return tag ID's as well
#     completed_date   : Optional[datetime] = None
#     deleted_date     : Optional[datetime] = None
#     completion_notes : Optional[ActionCompletedSchema] = None

# action_schema_dict = {
#     "id"               : int,
#     "title"            : str,
#     "description"      : str,
#     "created"          : datetime,
#     "energy"           : Optional[int],
#     "date"             : Optional[datetime], # todo: added this later instead of at start by accident, should work
#     "project"          : Optional[ProjectDBSchema],
#     "required_context" : Optional[list[TagDBSchema]],
#     "tags"             : Optional[list[TagDBSchema]], # todo: return tag ID's as well
#     "completed_date"   : Optional[datetime],
#     "deleted_date"     : Optional[datetime],
#     "completion_notes" : Optional[ActionCompletedSchema],
# }


class TestGetActionResponse(ActionDBSchema):
    completed : Optional[bool] = None

# class TestGetActionResponse2(Schema):
#     id: action_schema_dict["id"]

# https://django-ninja.dev/guides/input/filtering/
class ActionQueryFilterSchema(FilterSchema):
    #todo: add orderby
    title            : Optional[str]       = None
    project_id       : Optional[int]       = None
    energy           : Optional[int]       = None
    date             : Optional[datetime]  = None
    tags             : Optional[list[str]] = None
    required_context : Optional[list[str]] = None
    # todo: add this filter and use this for the order by
    completed        : Optional[bool]      = None

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
