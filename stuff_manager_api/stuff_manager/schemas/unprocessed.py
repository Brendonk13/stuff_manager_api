from ninja import Schema

class UnprocessedDBSchema(Schema):
    title: str
    description: str
    # user: int
    id: int
