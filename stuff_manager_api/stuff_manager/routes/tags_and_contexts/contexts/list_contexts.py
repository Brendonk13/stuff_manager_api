from ninja import Schema
from stuff_manager.models import Actions_RequiredContexts
from typing import Optional

class ContextDBSchema(Schema):
    id: int
    value: str

ListContextsResponse = list[Optional[ContextDBSchema]]

# todo: cannot paginate async yet
# https://github.com/vitalik/django-ninja/pull/1030/commits
# @paginate
def list_contexts(request):
    user = request.auth[0]
    data = []
    # todo: make another user and quickly test
    # TODO: DELETE DUPLICATES
    for action_context in Actions_RequiredContexts.objects.filter(action__user_id=user.id).select_related("tag").distinct("tag__id"):
        data.append({
            "id": action_context.tag.id,
            "value": action_context.tag.value
        })
    return data
