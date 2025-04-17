from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    parent_id: UUID | None = None

class UserOut(UserBase):
    id: UUID
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True
