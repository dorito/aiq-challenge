from tortoise.models import Model
from tortoise import fields

class Client(Model):
    guid = fields.UUIDField(primary_key=True)
    name = fields.TextField()
    email = fields.TextField(unique=True)
    hashed_password = fields.TextField()

    class PydanticMeta:
        exclude = ["hashed_password"]