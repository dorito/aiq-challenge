from tortoise.models import Model
from tortoise import fields

class ClientModel(Model):
    guid = fields.UUIDField(primary_key=True)
    name = fields.TextField()
    email = fields.CharField(255, unique=True)
    hashed_password = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    # TODO: adicionar roles
    
    class PydanticMeta:
        exclude = ["hashed_password"]

    class Meta:
        table = "client"