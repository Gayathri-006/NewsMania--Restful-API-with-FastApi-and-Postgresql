from pydantic import BaseModel, Field
from typing import List, Optional
from .base import BaseResponse

# Request schema for text summarization
class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=50, description="The news article text to summarize")
    max_length: Optional[int] = Field(150, description="Maximum length of the summary")
    num_key_points: Optional[int] = Field(3, description="Number of key points to extract")

# Response schema for text summarization
class SummaryResponse(BaseModel):
    summary: str
    key_points: List[str]
    length: int
    
    class Config:
        from_attributes = True

# AI response schema
class AIResponse(BaseResponse):
    data: Optional[SummaryResponse] = None
