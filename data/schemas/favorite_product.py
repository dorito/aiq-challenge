from pydantic import BaseModel

class CreateFavoriteProductSchema(BaseModel):
  product_id: int
