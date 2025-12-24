from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .base import BaseResponse

# Base news schema
class NewsBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    content: str = Field(..., min_length=10)
    summary: Optional[str] = None
    image_url: Optional[str] = None
    is_published: bool = True
    category_ids: List[int] = Field(default_factory=list)

# News create schema
class NewsCreate(NewsBase):
    pass

# News update schema
class NewsUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    content: Optional[str] = Field(None, min_length=10)
    summary: Optional[str] = None
    image_url: Optional[str] = None
    is_published: Optional[bool] = None
    category_ids: Optional[List[int]] = None

# News in DB schema (used for response)
class NewsInDB(NewsBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# News response with categories and author info
class NewsResponse(NewsInDB):
    categories: List['CategoryInNews'] = []
    author: 'AuthorInNews'

# Category in news response
class CategoryInNews(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True

# Author in news response
class AuthorInNews(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes = True

# News list response
class NewsListResponse(BaseResponse):
    data: List[NewsResponse] = []
    total: int
    page: int
    limit: int
    total_pages: int

# Single news response
class SingleNewsResponse(BaseResponse):
    data: Optional[NewsResponse] = None

# Update the forward references after all classes are defined
NewsResponse.update_forward_refs()
