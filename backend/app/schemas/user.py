from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    currency: str = "USD"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    currency: str | None = None
    password: str | None = None


class UserInDB(UserBase):
    id: int
    password_hash: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes: True


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str
