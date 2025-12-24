from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .base import BaseResponse
from .news import NewsResponse

# Base favorite schema
class FavoriteBase(BaseModel):
    news_id: int

# Favorite create schema
class FavoriteCreate(FavoriteBase):
    pass

# Favorite in DB schema
class FavoriteInDB(FavoriteBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Favorite response with news details
class FavoriteResponse(FavoriteInDB):
    news: Optional[NewsResponse] = None

# Favorite list response
class FavoriteListResponse(BaseResponse):
    data: List[FavoriteResponse] = []
    total: int
    page: int
    limit: int
    total_pages: int
