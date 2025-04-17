from pydantic import BaseModel, HttpUrl
from datetime import datetime

from app.utils.logs import get_logger

logger = get_logger(__name__)

class URLBase(BaseModel):
    original_url: HttpUrl


class URLCreate(URLBase):
    pass


class URLInfo(URLBase):
    id: int
    short_url: str
    created_at: datetime

    class Config:
        orm_mode = True

class URLUpdate(BaseModel):
    original_url: HttpUrl
    short_code: str

    class Config:
        orm_mode = True