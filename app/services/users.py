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
        user = await auth_client.register({
            "email": user_data.email,
            "password": user_data.password,
            "parent_id": str(user_data.parent_id)
        })
        logger.info(f"User registered in AUTH successfully: {user}")
        mlm_user = {
            "user_id": user.get("id"),
            "parent_id": str(user_data.parent_id)
        }
        response = await mlm_client.add_user(mlm_user)
        logger.info(f"User registered in MLM successfully: {response}")
        return user
    except Exception as e:
        # Handle registration error
        logger.error(f"Auth registration failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Auth registration failed: {str(e)}")
#         {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyM0BleGFtcGxlLmNvbSIsImV4cCI6MTc0NTAxMTUzN30.7uNGlC3EmMmpPQu1ksCweVJqCXYQZYEk3XTZ9VhIwZE",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyM0BleGFtcGxlLmNvbSIsImV4cCI6MTc0NzYwMjYzN30.ngbsSUMm6bfeSwPl1BJ0mkpH8j5YFUt3hu_BQ_rTmnQ",
#   "token_type": "bearer"
# }