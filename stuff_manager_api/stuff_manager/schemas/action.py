from django.db.models import Q
from ninja import FilterSchema
from typing import Optional
from datetime import datetime

# https://django-ninja.dev/guides/input/filtering/
class ActionQueryFilterSchema(FilterSchema):
    tags             : Optional[list[str]] = None
    required_context : Optional[list[str]] = None
    date             : Optional[datetime]  = None
    title            : Optional[str]       = None
    energy           : Optional[int]       = None
    project_id       : Optional[int]       = None

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
