from ninja import ModelSchema
from stuff_manager.models import Unprocessed

class UnprocessedDBSchema(ModelSchema):
    class Meta:
        model = Unprocessed
        fields = "__all__"

    # title: str
    # description: str
    # id: int
