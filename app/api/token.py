from fastapi import APIRouter, Header
from app.api_clients.auth import AuthApiClient
from app.schemas.token import Token
from app.utils.logs import get_logger

logger = get_logger(__name__)

router = APIRouter()
auth_client = AuthApiClient.prepare()

@router.post("/refresh", response_model=Token)
async def refresh_token(token: str = Header("Refresh Token")):
    return await auth_client.refresh(token)