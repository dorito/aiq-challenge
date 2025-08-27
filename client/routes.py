from fastapi import APIRouter, HTTPException, Request
from .service import ClientService
from data.schemas import ClientSchema, CreateClientSchema, EditClientSchema, LoginDataSchema, LoginTokenSchema

client_router = APIRouter()

@client_router.get("/")
async def list_clients() -> list[ClientSchema]:
    return await ClientService().list_clients()

@client_router.get("/by-email/{client_email}")
async def get_client_by_email(client_email: str) -> ClientSchema:
    client = await ClientService().get_client(email=client_email)
    if not client:
        raise HTTPException(status_code=404, detail="User not found")
    return client

@client_router.post("/")
async def create_client(client_data: CreateClientSchema) -> ClientSchema:
    return await ClientService().create_client(client_data)

@client_router.patch("/by-email/{client_email}")
async def edit_client(client_email: str, client_data: EditClientSchema) -> ClientSchema:
    return await ClientService().edit_client(client_email, client_data)

@client_router.delete("/by-email/{client_email}", status_code=204)
async def delete_client(client_email: str) -> None:
    await ClientService().remove_client(client_email)

@client_router.post("/login")
async def login_client(client_data: LoginDataSchema, request: Request) -> LoginTokenSchema:
    return await ClientService(cache=request.app.cache).login(client_data)