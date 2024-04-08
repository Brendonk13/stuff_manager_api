from ninja import Query
from stuff_manager.models import Action
from typing import Optional
from ninja import ModelSchema
from stuff_manager.schemas.action import ActionQueryFilterSchema, ActionDBSchema, OrderByList
from .utils.extract_action_data import extract_action_data


ListActionsResponseSchema = list[Optional[ActionDBSchema]]

def format_order_by(order_by_list: OrderByList):
    if not order_by_list:
        return []
    return [
        order_by.value.value if order_by.ascending else f"-{order_by.value.value}"
        for order_by
        in order_by_list
    ]

# todo: be able to search by regex in title, descriptions

# todo: cannot paginate async yet
# https://github.com/vitalik/django-ninja/pull/1030/commits
# @paginate
async def list_actions(request, query_filters: Query[ActionQueryFilterSchema]):
    print("query filters", type(query_filters), query_filters)
    # print(dir(query_filters))
    order_by = query_filters.order_by
    setattr(query_filters, "order_by", None)
    order_by = format_order_by(order_by)
    print("formatted order by", order_by)

    user = request.auth[0]
    data = [
        await extract_action_data(action)
        async for action
        in query_filters.filter(
            Action.objects.filter(user_id=user.id).select_related("project", "completion_notes")
        # ).distinct()
        ).order_by(*order_by)
    ]
    # todo: should the select related be outside of query_filters.filter ?
    # print("all actions", data)
    return data
