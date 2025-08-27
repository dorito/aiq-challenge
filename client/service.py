from typing import Optional
from fastapi import HTTPException
from typing import Optional
from data.schemas import CreateClientSchema, EditClientSchema, LoginDataSchema, LoginTokenSchema
from data.enums import LoginTokenTypeEnum
from data.models import ClientModel
from hashlib import sha256
from redis.asyncio import Redis
import datetime
import uuid

class ClientService:
  def __init__(self, cache: Optional[Redis] = None):
        self._cache = cache
        
  async def list_clients(self) -> list[ClientModel]:
      return await ClientModel.all()

  async def get_client(self, email: Optional[str] = None) -> ClientModel | None:
      if email:
          return await ClientModel.get_or_none(email=email)
      raise HTTPException(status_code=400, detail="Email must be provided")

  async def create_client(self, client_data: CreateClientSchema) -> ClientModel:
      if await self.get_client(email=client_data.email):
          raise HTTPException(status_code=400, detail="Email already registered")
      hashed_password = await self._get_hashed_password(client_data.password)
      client = ClientModel(**client_data.dict(), hashed_password=hashed_password)
      await client.save()
      return client

  async def edit_client(self, client_email: str, client_data: EditClientSchema) -> ClientModel:
      client = await ClientService().get_client(email=client_email)
      if not client:
        raise HTTPException(status_code=404, detail="User not found")
      hashed_current_password = await self._get_hashed_password(client_data.current_password)
      if not client_data.current_password or client.hashed_password != hashed_current_password:
          raise HTTPException(status_code=401, detail="Invalid current password")
      client.name = client_data.name or client.name
      if client_data.new_password:
          client.hashed_password = await self._get_hashed_password(client_data.new_password)
      await client.save()
      return client

  async def remove_client(self, client_email: str) -> None:
      client = await ClientService().get_client(email=client_email)
      if not client:
        raise HTTPException(status_code=404, detail="User not found")
      await client.delete()

  async def login(self, client_data: LoginDataSchema) -> LoginTokenSchema | None:
      login_time = 60*30 # 30 minutos de validade pro token de login
      client = await self.get_client(email=client_data.email)
      if not client:
          raise HTTPException(status_code=401, detail="Wrong password")
      if client.hashed_password != await self._get_hashed_password(client_data.password):
          raise HTTPException(status_code=401, detail="Wrong password")
      access_token = str(uuid.uuid4())
      await self._cache.set(f"token_{access_token}", client.email, login_time)
      return {"access_token": access_token, "token_type": LoginTokenTypeEnum.BEARER, "expires_in": datetime.datetime.now()+datetime.timedelta(seconds=login_time)}

  async def _get_hashed_password(self, password: str) -> str:
      return sha256(password.encode('utf-8')).hexdigest()