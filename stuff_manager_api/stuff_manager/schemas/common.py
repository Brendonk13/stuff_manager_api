from django.db.models import Q
from ninja import FilterSchema, Field
from typing_extensions import TypedDict
from typing import Optional
from datetime import datetime

class TagType(TypedDict):
    value: str


# https://django-ninja.dev/guides/input/filtering/
class ActionQueryFilterSchema(FilterSchema):
    # 
    tags: Optional[list[str]] = None
    # tags: Optional[list[str]] = Field(None, alias="actions_tags__value")
    # tags: Optional[list[TagType]] = None
    # required_context: Optional[list[TagType]] = None
    date: Optional[datetime] = None
    title: Optional[str] = None
    energy: Optional[int] = None

    # def filter_tags(self, value: bool) -> Q:
    # def filter_tags(self, value) -> Q:
    def filter_tags(self, _tags: Optional[list[str]]) -> Q:

        if not _tags:
            return Q()
        # tags = _tags[0].lstrip("[").rstrip("]")
        # tags = ["delegated", "someday_maybe"]
        # tags = ["delegated", "someday_maybe"]
        tags = ["usedOnceTag", "delegated"]
        # q_objects = Q() # Create an empty Q object to start with
        # for t in tags:
        #     print(t)
        #     q_objects |= Q(actions_tags__tag__value=t)
        q_objects = Q(actions_tags__tag__value__in=tags)
        print("filter thing", tags)
        return q_objects
        # return Q(action__tag__value=
        # return Q(view_count__gt=1000) | Q(download_count__gt=100) if value else Q()

