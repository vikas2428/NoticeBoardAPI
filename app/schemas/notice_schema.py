from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class NoticeCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=10)
    category: str = Field(..., min_length=3, max_length=50)
    expiry_date: Optional[date] = None


class NoticeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=10)
    category: Optional[str] = Field(None, min_length=3, max_length=50)
    expiry_date: Optional[date] = None
    status: Optional[str] = None


class NoticeResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    created_at: str
    expiry_date: Optional[str]
    status: str