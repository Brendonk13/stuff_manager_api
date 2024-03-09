from ninja import Schema
from stuff_manager.models import Unprocessed
from ninja.errors import HttpError

class DeleteUnprocessedResponseSchema(Schema):
    message: str

async def delete_unprocessed(request, unprocessed_id: int):
    user = request.auth[0]
    try:
        unprocessed = await Unprocessed.objects.aget(id=unprocessed_id)
    except Unprocessed.DoesNotExist:
        raise HttpError(404, "Unprocessed not found")

    if unprocessed.user_id != user.id:
        return 403, { "message": "Unauthorized" }
    await unprocessed.adelete()
    return {
        "message": "Success",
    }

