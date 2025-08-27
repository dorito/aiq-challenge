from data.models import FavoriteProductModel, ClientModel
from data.schemas import CreateFavoriteProductSchema, ProductSchema
from redis.asyncio import Redis
from fastapi import HTTPException
from typing import Optional
from product.service import ProductService

class FavoriteProductService:
    def __init__(self, cache: Optional[Redis] = None, product_service: Optional[ProductService] = None):
        self._cache = cache
        self._product_service = product_service

    async def list_favorite_products(self, client: ClientModel) -> list[ProductSchema]:
        favorite_products = await FavoriteProductModel.filter(client_guid=client.guid).all()
        return [await self._product_service.get_product(fp.product_id) for fp in favorite_products]

    async def get_favorite_product(self, product_id: int, client: ClientModel) -> ProductSchema | None:
        favorite_product = await FavoriteProductModel.get_or_none(product_id=product_id, client_guid=client.guid)
        if not favorite_product:
            raise HTTPException(status_code=404, detail="Favorite product not found")
        return await self._product_service.get_product(product_id)

    async def add_favorite_product(self, favorite_product_data: CreateFavoriteProductSchema, client: ClientModel) -> ProductSchema:
        favorite_product = await FavoriteProductModel.get_or_none(product_id=favorite_product_data.product_id, client_guid=client.guid)
        if favorite_product:
            raise HTTPException(status_code=400, detail="Favorite product already exists")
        favorite_product = FavoriteProductModel(product_id=favorite_product_data.product_id, client_guid=client.guid)
        await favorite_product.save()
        return await self._product_service.get_product(favorite_product_data.product_id)

    async def remove_favorite_product(self, product_id: int, client: ClientModel) -> None:
        favorite_product = await FavoriteProductModel.get_or_none(product_id=product_id, client_guid=client.guid)
        if not favorite_product:
            raise HTTPException(status_code=404, detail="Favorite product not found")
        await favorite_product.delete()
