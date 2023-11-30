from ninja import Schema
from stuff_manager.models import Unprocessed
from ninja.errors import HttpError

class UnprocessedDBSchema(Schema):
    title: str
    description: str

class GetUnprocessedResponseSchema(Schema):
    message: str
    data: UnprocessedDBSchema

# class GetUnprocessedSchema(Schema):
#     title: str
#     description: str

# how to get number from param
async def get_unprocessed(request, unprocessed_id):
    print(f"id: {unprocessed_id}")
    try:
        unprocessed = await Unprocessed.objects.aget(id=unprocessed_id)
        print(f"unprocessed: {unprocessed}")
    except Unprocessed.DoesNotExist:
        raise HttpError(404, "Unprocessed item not found")
    return {
        "message": "Success",
        "data": unprocessed,
    }
