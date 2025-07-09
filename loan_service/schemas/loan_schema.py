from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LoanCreate(BaseModel):
    user_id: str
    book_id: str
    due_date: datetime

class ReturnRequest(BaseModel):
    loan_id: str

class LoanOut(BaseModel):
    id: str
    user_id: str 
    book_id: str
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str

class LoanBookInfo(BaseModel):
    id: str
    title: str
    author: str

class LoanWithBook(BaseModel):
    id: str
    book: LoanBookInfo
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str

class LoanDetails(BaseModel):
    id: str
    user: dict
    book: dict
    issue_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str 