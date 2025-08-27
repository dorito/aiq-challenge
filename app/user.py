from fastapi  import Request, HTTPException
from client.service import ClientService
from data.models import ClientModel

async def get_client_by_token(request: Request) -> ClientModel:
    service = ClientService()
    cache = request.app.cache
    token = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
    cached_email = await cache.get(f"token_{token}")
    if cached_email is not None:
        cached_email = cached_email.decode("utf-8")
    client = await service.get_client(email=cached_email) if cached_email else None
    if client is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return client