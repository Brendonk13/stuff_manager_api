from ninja import Schema
from stuff_manager.models import Action, Unprocessed, unprocessed
from typing import Optional
from stuff_manager.schemas.unprocessed import UnprocessedDBSchema

class ListUnprocessedResponseSchema(Schema):
    message: str
    data: list[Optional[UnprocessedDBSchema]]

async def get_all_unprocessed(user_id: int):
    return [
        unprocessed
        async for unprocessed
        in Unprocessed.objects.filter(user_id=user_id)
    ]


async def get_unprocessed_items(user_id: int):
    all_unprocessed = await get_all_unprocessed(user_id)
    all_unprocessed_ids = set(u.id for u in all_unprocessed)

    # processed unprocessed's
    unprocessed_ids_with_actions = set([
        action.unprocessed_id
        async for action
        in Action.objects.filter(user_id=user_id, unprocessed_id__in=all_unprocessed_ids)
    ])

    unprocessed_ids = all_unprocessed_ids - unprocessed_ids_with_actions
    return [u for u in all_unprocessed if u.id in unprocessed_ids]
    # return filter(all_unprocessed, lambda u: u.id in unprocessed_ids)


async def list_unprocessed(request):
    # Note: this only returns Unprocessed items WITHOUT corresponding actions
    # ie: return the unprocessed's which have not been processed
    user = request.auth[0]
    unprocessed_items = await get_unprocessed_items(user.id)
    print(f"unprocessed ({len(unprocessed_items)}) for user: {unprocessed_items}")
    return {
        "message": "Success",
        "data": unprocessed_items,
    }

