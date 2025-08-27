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

async def favorite_product_service(request: Request):
    return FavoriteProductService(cache=request.app.cache, product_service=ProductService(cache=request.app.cache))

@favorite_product_router.get("/")
async def list_favorite_products(client: Annotated[ClientModel, Depends(get_client_by_token)], service: Annotated[FavoriteProductService, Depends(favorite_product_service)], token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> list[ProductSchema]:
    return await service.list_favorite_products(client=client)

@favorite_product_router.post("/", status_code=201)
async def add_favorite_product(favorite_product_data: CreateFavoriteProductSchema, client: Annotated[ClientModel, Depends(get_client_by_token)], service: Annotated[FavoriteProductService, Depends(favorite_product_service)], token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> ProductSchema:
    return await service.add_favorite_product(favorite_product_data, client=client)

@favorite_product_router.delete("/by-product-id/{product_id}", status_code=204)
async def delete_favorite_product(product_id: int, client: Annotated[ClientModel, Depends(get_client_by_token)], service: Annotated[FavoriteProductService, Depends(favorite_product_service)], token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> None:
    await service.remove_favorite_product(product_id=product_id, client=client)