from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from ..schemas.base import BaseResponse

# User base schema
class UserBase(BaseModel):
    email: EmailStr
    name: str

# User create schema (for registration)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one number')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v

# User update schema
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None

# User in DB schema
class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# User response schema
class UserResponse(BaseResponse):
    data: Optional[UserInDB] = None

# User login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Token response schema
class TokenResponse(BaseResponse):
    access_token: str
    token_type: str

# User registration response
class UserRegistrationResponse(BaseResponse):
    data: Optional[UserInDB] = None

# User login response
class UserLoginResponse(BaseResponse):
    data: Optional[TokenResponse] = None
