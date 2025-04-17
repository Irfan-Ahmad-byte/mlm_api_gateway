from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.redis import check_redis_connection
from app.utils.logs import get_logger

r = check_redis_connection()
logger = get_logger(__name__)

class RateLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit: int = 10, window_seconds: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window_seconds

    async def dispatch(self, request: Request, call_next):
        identifier = request.headers.get("Authorization") or request.client.host
        key = f"rate-limit:{identifier}"

        current_count = r.get(key)
        if current_count is None:
            r.set(key, 1, ex=self.window)
        elif int(current_count) < self.limit:
            r.incr(key)
        else:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later."
            )

        response = await call_next(request)
        return response
