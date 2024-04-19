from ninja import Query
from stuff_manager.models import Action
from typing import Optional
# from ninja import ModelSchema
from stuff_manager.schemas.action import ActionQueryFilterSchema, ActionDBSchema
from .utils.extract_action_data import extract_action_data


ListActionsResponseSchema = list[Optional[ActionDBSchema]]

def extract_order_by_pairs(order_by_list):
    """
        order by query string format explained:
        order_by = [title,True,created,False] ==> order by title ascending, then created descending -- must extract pairs
    """
    order_by_list = order_by_list.lstrip("[").rstrip("]").split(",")

    for idx in range(0, len(order_by_list), 2):
        field_name, ascending = order_by_list[idx], order_by_list[idx + 1]
        ascending = True if ascending == "true" else False

        if field_name == "completed":
            field_name = "completed_date"
        if field_name == "deleted":
            field_name = "deleted_date"
        yield field_name, ascending

def format_order_by(order_by_list: Optional[str]):
# def format_order_by(order_by_list: Optional[list[str]]):
    if not order_by_list:
        return []
    return [
        value if ascending else f"-{value}"
        for value, ascending
        in extract_order_by_pairs(order_by_list)
    ]

    # ret = []
    # for value, ascending in extract_order_by_pairs(order_by_list):
    #     print("value, ascending", value, ascending)
    #     ret.append(value if ascending else f"-{value}")
    # return ret



# todo: be able to search by regex in title, descriptions
# todo: cannot paginate async yet
# https://github.com/vitalik/django-ninja/pull/1030/commits
# @paginate
async def list_actions(request, query_filters: Query[ActionQueryFilterSchema]):
    print("query filters", type(query_filters), query_filters)
    order_by = query_filters.order_by

    # order_by is not a field on the model so make sure we dont filter by this value
    setattr(query_filters, "order_by", None)
    order_by = format_order_by(order_by)
    print("formatted order by", order_by)

    user = request.auth[0]
    data = [
        await extract_action_data(action)
        async for action
        in query_filters.filter(
            Action.objects.filter(user_id=user.id).select_related("project", "completion_notes")
        ).order_by(*order_by)
    ]
    # todo: should the select related be outside of query_filters.filter ?
    # print("all actions", data)
    return data
