# from stuff_manager.models import Projects_User
# from ninja import Schema
from stuff_manager.models import Unprocessed
from ninja.errors import HttpError
from stuff_manager.schemas.unprocessed import UnprocessedDBSchema

GetUnprocessedResponseSchema = UnprocessedDBSchema


async def get_unprocessed(request, unprocessed_id):
    print(f"id: {unprocessed_id}")
    user = request.auth[0]
    try:
        unprocessed = await Unprocessed.objects.aget(id=unprocessed_id)
        print(f"unprocessed: {unprocessed}")
        if user.id != unprocessed.user_id:
            return 403, { "message": "Unauthorized", "data": None }
        return unprocessed

    except Unprocessed.DoesNotExist:
        raise HttpError(404, "Unprocessed item not found")
