from pydantic import BaseModel
from datetime import datetime

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
    user_id: str
    book_id: str
    issue_date: datetime
    due_date: datetime
    return_date: datetime | None = None
    status: str
