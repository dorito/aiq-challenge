import uuid
from pydantic import BaseModel, EmailStr
import datetime
from data.enums import LoginTokenTypeEnum

class ClientSchema(BaseModel):
    guid: uuid.UUID
    name: str
    email: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class CreateClientSchema(BaseModel):
    name: str
    email: EmailStr
    password: str

class EditClientSchema(BaseModel):
    name: str | None = None
    new_password: str | None = None
    current_password: str

class LoginDataSchema(BaseModel):
    email: EmailStr
    password: str

class LoginTokenSchema(BaseModel):
    access_token: uuid.UUID
    token_type: LoginTokenTypeEnum
    expires_in: datetime.datetime