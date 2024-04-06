from typing import Optional
from ninja import Schema
from stuff_manager.models import Unprocessed
from stuff_manager.schemas.unprocessed import UnprocessedDBSchema

CreateUnprocessedResponseSchema = UnprocessedDBSchema

class CreateUnprocessedSchema(Schema):
    title: str
    description: Optional[str] = ""

async def create_unprocessed(request, data: CreateUnprocessedSchema):
    print(f'data: {data}')
    user = request.auth[0]
    new_item = await Unprocessed.objects.acreate(**{**data.dict(), "user": user})
    print(f"new_item: {new_item}")
    # print(f"new_item: {dir(new_item)}")
    print(f"new item id: {new_item.id}")
    return new_item
