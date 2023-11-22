from ninja import Schema
from stuff_manager.models import Unprocessed

class UnprocessedSchema(Schema):
    title: str
    description: str
    # user: int

    # @staticmethod
    # def resolve_user(obj, context):
    #     user = context['request'].auth[0]
    #     return user.id


async def create_unprocessed(request, data: UnprocessedSchema):
    print(f'data: {data}')
    user = request.auth[0]
    new_item = await Unprocessed.objects.acreate(**{**data.dict(), "user": user})
    print(f"new_item: {new_item}")
    print(f"new_item: {dir(new_item)}")
    return {
        "message": "Success",
        "id": new_item.id,
    }
