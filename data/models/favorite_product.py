from tortoise.models import Model
from tortoise import fields

class FavoriteProductModel(Model):
    guid = fields.UUIDField(primary_key=True)
    client_guid = fields.UUIDField()
    product_id = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "favorite_product"