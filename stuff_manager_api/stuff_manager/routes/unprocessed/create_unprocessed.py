from ninja import Schema
from stuff_manager.models import Unprocessed

# class DefaultResponseSchema(Schema):
#     message: str

class UnprocessedDBSchema(Schema):
    title: str
    description: str
    # user: int
    id: int

    # @staticmethod
    # def resolve_user(obj, context):
    #     user = context['request'].auth[0]
    #     return user.id



class CreateUnprocessedResponseSchema(Schema):
    message: str
    data: UnprocessedDBSchema

class CreateUnprocessedSchema(Schema):
    title: str
    description: str
    # user: int

    # @staticmethod
    # def resolve_user(obj, context):
    #     user = context['request'].auth[0]
    #     return user.id


async def create_unprocessed(request, data: CreateUnprocessedSchema):
    print(f'data: {data}')
    user = request.auth[0]
    new_item = await Unprocessed.objects.acreate(**{**data.dict(), "user": user})
    print(f"new_item: {new_item}")
    # print(f"new_item: {dir(new_item)}")
    print(f"new item id: {new_item.id}")
    return {
        "message": "Success",
        "data": new_item,
    }
