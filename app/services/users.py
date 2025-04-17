from fastapi import HTTPException
from app.api_clients.mlm import MLMApiClient
from app.api_clients.auth import AuthApiClient

from app.schemas.user import UserCreate, UserOut
from app.utils.logs import get_logger
logger = get_logger(__name__)

async def register_user(user_data: UserCreate):
    """
    Register a new user in the Auth and then MLM system.
    """
    auth_client = AuthApiClient.prepare()
    mlm_client = MLMApiClient.prepare()

    try:
        response = await auth_client.register(user_data.model_dump())
        user = UserOut.model_validate_json(response)
        mlm_user = {
            "user_id": user.id,
            "parent_id": user_data.parent_id
        }
        response = await mlm_client.add_user(mlm_user)
        return response
    except Exception as e:
        # Handle registration error
        logger.error(f"Auth registration failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Auth registration failed: {str(e)}")
        