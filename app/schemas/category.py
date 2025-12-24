from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .base import BaseResponse

# Base category schema
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)

# Category create schema
class CategoryCreate(CategoryBase):
    pass

# Category update schema
class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)

# Category in DB schema
class CategoryInDB(CategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Category response with news count
class CategoryResponse(CategoryInDB):
    news_count: int = 0

# Category list response
class CategoryListResponse(BaseResponse):
    data: List[CategoryResponse] = []
    total: int
    page: int
    limit: int
    total_pages: int

# Single category response
class SingleCategoryResponse(BaseResponse):
    data: Optional[CategoryResponse] = None
