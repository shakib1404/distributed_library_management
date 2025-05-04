# ✅ app/schemas/loan_schema.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LoanCreate(BaseModel):
    user_id: str
    book_id: str
    due_date: datetime

class ReturnRequest(BaseModel):
    loan_id: str

class ExtendRequest(BaseModel):
    extension_days: int

class LoanOut(BaseModel):
    id: str
    user_id: Optional[str] = None
    book_id: Optional[str] = None
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str

class LoanExtendOut(LoanOut):
    extensions_count: int

class BookInfo(BaseModel):
    id: str
    title: str
    author: str

class LoanWithBookOut(BaseModel):
    id: str
    book: BookInfo
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str
