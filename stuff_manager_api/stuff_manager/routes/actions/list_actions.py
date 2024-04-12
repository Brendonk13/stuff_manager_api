from ninja import Query
from stuff_manager.models import Action
from typing import Optional
from ninja import ModelSchema
from stuff_manager.schemas.action import ActionQueryFilterSchema, ActionDBSchema, OrderByList
from .utils.extract_action_data import extract_action_data


ListActionsResponseSchema = list[Optional[ActionDBSchema]]

def get_order_by_pairs(order_by_list):
    print("original, ", order_by_list, type(order_by_list))
    pairs = [[]]
    count = 0
    for order_by in order_by_list.lstrip("[").rstrip("]").split(","):
        # order_by = order_by.strip("\"'").lstrip("[").rstrip("]").strip("\"'").split(",")
        print("count", count,"after stripping order by", order_by)
        if count % 2 == 1:
            order_by = False if order_by == "false" else True

        if order_by == "completed":
            order_by = "completed_date"
        if order_by == "deleted":
            order_by = "deleted_date"

        # print("about to append order by", order_by)
        pairs[-1].append(order_by)
        # pairs[-1].append(order_by)
        if count % 2 == 1:
            pairs.append([])
        count += 1
    if not pairs[-1]:
        pairs.pop()
    print("pairs", pairs)
    return pairs

def format_order_by(order_by_list: Optional[str]):
# def format_order_by(order_by_list: Optional[list[str]]):
    if not order_by_list:
        return []
    ret = []
    for value, ascending in get_order_by_pairs(order_by_list):
        print("value, ascending", value, ascending)
        ret.append(value if ascending else f"-{value}")
    return ret
    # return [
    #     # order_by.value.value if order_by.ascending else f"-{order_by.value.value}"
    #     value if ascending else f"-{value}"
    #     for value, ascending
    #     in get_order_by_pairs(order_by_list)
    # ]

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
