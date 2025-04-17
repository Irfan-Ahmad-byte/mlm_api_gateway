from fastapi import APIRouter, HTTPException

from app.api_clients.url_shortner import UrlShortenerApiClient
from app.schemas.url import URLCreate, URLInfo
from app.utils.logs import get_logger

logger = get_logger(__name__)
router = APIRouter()
shortener_client = UrlShortenerApiClient.prepare()

@router.post("/shorten", response_model=URLInfo)
async def shorten_url(url: URLCreate):
    original_url = str(url.original_url)
    if not original_url:
        logger.error("Missing original_url")
        raise HTTPException(status_code=400, detail="Missing original_url")
    return await shortener_client.shorten(original_url)

@router.get("/{short_code}")
async def redirect(short_code: str):
    return await shortener_client.redirect(short_code)
