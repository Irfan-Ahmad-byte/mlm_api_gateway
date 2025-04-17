from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.redis import check_redis_connection
from app.middlewares.rate_limiter import RateLimiterMiddleware
from app.middlewares.request_logger import RequestLoggingMiddleware
from app.utils.logs import get_logger
from app.api import auth, exchange, url_shortner

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    logger.info("Connecting to redis...")
    check_redis_connection()
    # Perform any startup tasks here
    logger.info("Application's ready...")
    yield
    print("Shutting down...")


app = FastAPI(title="Exchange API Gateway", version="1.0.0", lifespan=lifespan)
app.add_middleware(RateLimiterMiddleware, limit=10, window_seconds=60)
app.add_middleware(
    # Middleware for logging requests
    RequestLoggingMiddleware
)

@app.get("/")
async def root():
    return {"message": "Welcome to Exchange API"}
@app.get("/health")
async def health():
    return {"status": "healthy"}
@app.get("/status")
async def status():
    return {"status": "running"}


app.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Authentication"]
    # dependencies=[Depends(get_db)],  # Uncomment if you want to use the dependency for all routes, since we're checking the DB connection on startup, no need to add here
    # include_in_schema=False,  # Uncomment if you want to exclude this router from the OpenAPI schema
    # default_response_class=JSONResponse,  # Uncomment if you want to set a default response class
)
app.include_router(exchange.router, prefix="/exchange", tags=["Exchange"])
app.include_router(url_shortner.router, prefix="/url-shortner", tags=["URL Shortner"])