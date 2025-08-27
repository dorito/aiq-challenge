from typing import Annotated
from fastapi import APIRouter, HTTPException, Request, Depends
from .service import ClientService
from data.schemas import ClientSchema, CreateClientSchema, EditClientSchema, LoginDataSchema, LoginTokenSchema

client_router = APIRouter()

async def client_service(request: Request):
    return ClientService(cache=request.app.cache)
  
@client_router.get("/")
async def list_clients(service: Annotated[ClientService, Depends(client_service)]) -> list[ClientSchema]:
    return await service.list_clients()

@client_router.get("/by-email/{client_email}")
async def get_client_by_email(client_email: str, service: Annotated[ClientService, Depends(client_service)]) -> ClientSchema:
    client = await service.get_client(email=client_email)
    if not client:
        raise HTTPException(status_code=404, detail="User not found")
    return client

@client_router.post("/", status_code=201)
async def create_client(client_data: CreateClientSchema, service: Annotated[ClientService, Depends(client_service)]) -> ClientSchema:
    return await service.create_client(client_data)

@client_router.patch("/by-email/{client_email}")
async def edit_client(client_email: str, client_data: EditClientSchema, service: Annotated[ClientService, Depends(client_service)]) -> ClientSchema:
    return await service.edit_client(client_email, client_data)

@client_router.delete("/by-email/{client_email}", status_code=204)
async def delete_client(client_email: str, service: Annotated[ClientService, Depends(client_service)]) -> None:
    await service.remove_client(client_email)

@client_router.post("/login")
async def login_client(client_data: LoginDataSchema, request: Request, service: Annotated[ClientService, Depends(client_service)]) -> LoginTokenSchema:
    return await service.login(client_data)