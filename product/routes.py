from typing import Annotated
from fastapi import APIRouter, Depends, Request
from .service import ProductService
from data.schemas import ProductSchema

product_router = APIRouter()

async def product_service(request: Request):
    return ProductService(cache=request.app.cache)

@product_router.get("/")
async def list_products(service: Annotated[ProductService, Depends(product_service)]) -> list[ProductSchema]:
    return await service.list_products()

@product_router.get("/by-id/{product_id}")
async def get_product_by_id(product_id: int, service: Annotated[ProductService, Depends(product_service)]) -> ProductSchema:
    product = await service.get_product(id=product_id)
    return product
