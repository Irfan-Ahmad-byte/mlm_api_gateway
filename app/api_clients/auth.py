from fastapi.security import OAuth2PasswordRequestForm
from app.api_clients.client import ApiClient
from app.configs.configs import settings
from app.utils.logs import get_logger

logger = get_logger(__name__)

class AuthApiEndPoints:
    REGISTER = "/auth/register"
    LOGIN = "/auth/login"
    LOGOUT = "/auth/logout"
    REFRESH = "/auth/refresh"
    ME = "/users/me"
    LOGIN_HISTORY = "/users/login-history"


class AuthApiClient:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    @staticmethod
    def prepare() -> "AuthApiClient":
        base_url = settings.AUTH_BASE_URL
        api_key = settings.AUTH_API_KEY
        api_secret = settings.AUTH_API_SECRET

        if not base_url:
            logger.error("Environment variables for AUTH API are missing")
            raise EnvironmentError("Required environment variables are not set.")

        headers = {
            "X-Api-Key": api_key,
            "X-Api-Secret": api_secret
        }

        return AuthApiClient(ApiClient(base_url, headers))

    # Register a new user
    async def register(self, user_data: dict):
        return await self.api_client.post(AuthApiEndPoints.REGISTER, body=user_data)

    # Login and get tokens
    async def login(self, credentials: OAuth2PasswordRequestForm):
        return await self.api_client.post(AuthApiEndPoints.LOGIN, body={}, form_data={i: credentials.__dict__[i] for i in credentials.__dict__ if i != "client"})

    # Logout user by blacklisting refresh token
    async def logout(self, refresh_token: str):
        headers = {"refresh_token": refresh_token}
        return await self.api_client.post(AuthApiEndPoints.LOGOUT, body={}, headers=headers)

    # Refresh access token
    async def refresh(self, refresh_token: str):
        headers = {"refresh_token": refresh_token}
        return await self.api_client.post(AuthApiEndPoints.REFRESH, body={}, headers=headers)

    # Get user info using access token
    async def get_user(self, access_token: str):
        headers = {"Token": f"Bearer {access_token}"}
        return await self.api_client.get(AuthApiEndPoints.ME, headers=headers)

    # Get user login history using access token
    async def get_login_history(self, access_token: str):
        headers = {"Token": f"Bearer {access_token}"}
        return await self.api_client.get(AuthApiEndPoints.LOGIN_HISTORY, headers=headers)



# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ0NTMxNTEzfQ.crfyI3uTdIkhTbjRNT3D3eSUTFJnvsigGBs1OSnIfqE
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyQGV4YW1wbGUuY29tIiwiZXhwIjoxNzQ3MTIyNjEzfQ.G4H6_g8Wd3sxI1LluHG5nKdkmRIlGXbvnoMRve0WL8g