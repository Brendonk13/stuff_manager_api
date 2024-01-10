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

#     def custom_expression(self) -> Q:
#         q = Q()
#         if self.title:
#             q &= Q(title=self.title)
#         if self.energy:
#             q &= Q(energy=self.energy)
#         if self.date: # todo: fix this to work with dates and not datetimes
#             q &= Q(date=self.date)
#         # parse query string

#         # todo: what happens if a context and a tag have the same name ????
#         # tags = []
#         if self.tags:
#             tags = [tag.strip("\"'") for tag in self.tags[0].rstrip("]").lstrip("[").split(",")]
#             q &= Q(tag__value__in=tags)
#         if self.required_context:
#             tags = [tag.strip("\"'") for tag in self.required_context[0].rstrip("]").lstrip("[").split(",")]
#             q &= Q(tag__value__in=tags)

#         # if self.tags or self.required_context:
#             # q &= Q(tag__value__in=tags)
#         print(q)
#         return q

    def filter_tags(self, _tags: Optional[list[str]]) -> Q:
        if not _tags:
            return Q()
        # parse query string
        tags = [tag.strip("\"'") for tag in _tags[0].rstrip("]").lstrip("[").split(",")]
        # return Q(tag__value__in=tags)
        return Q(actions_tags__tag__value__in=tags)

    def filter_required_context(self, _tags: Optional[list[str]]) -> Q:

        if not _tags:
            return Q()
        # parse query string
        tags = [tag.strip("\"'") for tag in _tags[0].rstrip("]").lstrip("[").split(",")]
        # return Q(tag__value__in=tags)
        return Q(actions_requiredcontexts__tag__value__in=tags)
