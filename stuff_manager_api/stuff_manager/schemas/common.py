from django.db.models import Q
from ninja import FilterSchema, Field
from typing_extensions import TypedDict
from typing import Optional
from datetime import datetime

class TagType(TypedDict):
    value: str


# https://django-ninja.dev/guides/input/filtering/
class ActionQueryFilterSchema(FilterSchema):
    tags: Optional[list[str]] = None
    required_context: Optional[list[str]] = None
    date: Optional[datetime] = None
    title: Optional[str] = None
    energy: Optional[int] = None

    # def filter_tags(self, value: bool) -> Q:
    # def filter_tags(self, value) -> Q:
    def filter_tags(self, _tags: Optional[list[str]]) -> Q:
        # return self.filter_required_context(_tags)
        if not _tags:
            return Q()
        # parse query string
        tags = [tag.strip("\"'") for tag in _tags[0].rstrip("]").lstrip("[").split(",")]

        q_objects = Q(actions_tags__tag__value__in=tags)
        return q_objects

    def filter_required_context(self, _tags: Optional[list[str]]) -> Q:

        if not _tags:
            return Q()
        # parse query string
        tags = [tag.strip("\"'") for tag in _tags[0].rstrip("]").lstrip("[").split(",")]

        # q_objects = Q() # Create an empty Q object to start with
        # for t in tags:
        #     print(t)
        #     q_objects &= Q(actions_tags__tag__value=t)

        q_objects = Q(actions_requiredcontexts__tag__value__in=tags)
        return q_objects
