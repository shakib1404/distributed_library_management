from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    copies: int

class BookUpdate(BaseModel):
    copies: Optional[int]
    available_copies: Optional[int]

class BookOut(BookCreate):
    id: str
    available_copies: int
    created_at: datetime
    updated_at: datetime