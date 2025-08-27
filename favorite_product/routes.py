from typing import Annotated
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import APIRouter, Depends, Request
from .service import FavoriteProductService
from product.service import ProductService
from data.schemas import ProductSchema, CreateFavoriteProductSchema
from data.models import ClientModel
from app.user import get_client_by_token

favorite_product_router = APIRouter()
auth_scheme = HTTPBearer()

@favorite_product_router.get("/")
async def list_favorite_products(request: Request, client: Annotated[ClientModel, Depends(get_client_by_token)], token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> list[ProductSchema]:
    return await FavoriteProductService(cache=request.app.cache, product_service=ProductService(cache=request.app.cache)).list_favorite_products(client=client)

@favorite_product_router.post("/")
async def add_favorite_product(request: Request, favorite_product_data: CreateFavoriteProductSchema, client: Annotated[ClientModel, Depends(get_client_by_token)], token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> ProductSchema:
    return await FavoriteProductService(cache=request.app.cache, product_service=ProductService(cache=request.app.cache)).add_favorite_product(favorite_product_data, client=client)

@favorite_product_router.delete("/by-product-id/{product_id}", status_code=204)
async def delete_favorite_product(product_id: int, client: Annotated[ClientModel, Depends(get_client_by_token)], token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> None:
    await FavoriteProductService().remove_favorite_product(product_id=product_id, client=client)