# ✅ app/routers/loan_router.py
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.loan_schema import LoanCreate, ReturnRequest, ExtendRequest, LoanOut, LoanExtendOut, LoanWithBookOut
from app.services.loan_service import LoanService

router = APIRouter(prefix="/api", tags=["Loans"])
loan_service = LoanService()

@router.post("/loans", response_model=LoanOut)
def issue_book(loan: LoanCreate):
    response = loan_service.issue_book(loan.dict())
    if "return_date" in response:
        del response["return_date"]
    return response

@router.post("/returns", response_model=LoanOut)
def return_book(req: ReturnRequest):
    return loan_service.return_book(req.loan_id)

@router.get("/loans/overdue")
def get_overdue():
    return loan_service.get_overdue_loans()

@router.put("/loans/{loan_id}/extend", response_model=LoanExtendOut)
def extend_loan(loan_id: str, req: ExtendRequest):
    loan = loan_service.extend_loan(loan_id, req.extension_days)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan

@router.get("/loans/{user_id}", response_model=List[LoanWithBookOut])
def user_loans(user_id: str):
    return loan_service.get_loans_by_user(user_id)
