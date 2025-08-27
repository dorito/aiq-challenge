from client.routes import client_router
from product.routes import product_router
from favorite_product.routes import favorite_product_router
from fastapi import FastAPI
from tortoise.contrib.fastapi import tortoise_exception_handlers
from app.lifespan import AppLifespans

app = FastAPI(
    lifespan=AppLifespans,
    exception_handlers=tortoise_exception_handlers()
)
app.include_router(client_router, prefix="/client", tags=["Client"])
app.include_router(product_router, prefix="/product", tags=["Product"])
app.include_router(favorite_product_router, prefix="/favorite-product", tags=["Favorite Product"])
