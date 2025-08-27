from fastapi import HTTPException
import requests
import json
from redis.asyncio import Redis
from data.schemas import ProductSchema

class ProductService:
    def __init__(self, cache: Redis):
        self._cache = cache

    async def list_products(self):
        cache_key = "all_products"
        cache_ttl = 60*5
        cached_data = await self._cache.get(cache_key)
        if cached_data:
            return json.loads(cached_data)

        response = requests.get("https://fakestoreapi.com/products")
        if response.status_code == 200:
            data = response.json()
            await self._cache.set(cache_key, json.dumps(data), cache_ttl)
            return [ProductSchema(**item) for item in data]
        return []
    
    async def get_product(self, id: int) -> ProductSchema:
        cache_key = f"product_{id}"
        cache_ttl = 60*5
        cached_data = await self._cache.get(cache_key)
        if cached_data:
            return ProductSchema(**json.loads(cached_data))

        response = requests.get(f"https://fakestoreapi.com/products/{id}")
        if response.status_code == 200:
            data = response.json()
            await self._cache.set(cache_key, json.dumps(data), cache_ttl)
            return ProductSchema(**data)
        raise HTTPException(status_code=404, detail="Product not found")