from app.api_clients.client import ApiClient
from app.configs.configs import settings
from app.utils.logs import get_logger

logger = get_logger(__name__)

class UrlShortenerEndpoints:
    SHORTEN = "/shorten"
    REDIRECT = "/{short_code}"


class UrlShortenerApiClient:
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    @staticmethod
    def prepare() -> "UrlShortenerApiClient":
        base_url = settings.SHORTENER_BASE_URL
        api_key = settings.SHORTENER_API_KEY
        api_secret = settings.SHORTENER_API_SECRET

        if not base_url:
            logger.error("Environment variables for SHORTENER API are missing")
            raise EnvironmentError("Required environment variables are not set.")

        headers = {
            "X-Api-Key": api_key,
            "X-Api-Secret": api_secret
        }

        return UrlShortenerApiClient(ApiClient(base_url, headers))

    async def shorten(self, original_url: str):
        return await self.api_client.post(
            UrlShortenerEndpoints.SHORTEN,
            body={"original_url": original_url}
        )

    async def redirect(self, short_code: str):
        return await self.api_client.get(UrlShortenerEndpoints.REDIRECT.format(short_code=short_code))
