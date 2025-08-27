from fastapi import APIRouter, HTTPException, Request
from .service import ProductService
from data.schemas import ProductSchema

product_router = APIRouter()

@product_router.get("/")
async def list_products(request: Request) -> list[ProductSchema]:
    return await ProductService(cache=request.app.cache).list_products()

@product_router.get("/by-id/{product_id}")
async def get_product_by_id(product_id: int, request: Request) -> ProductSchema:
    product = await ProductService(cache=request.app.cache).get_product(id=product_id)
    return product
