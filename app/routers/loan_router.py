from fastapi import APIRouter, HTTPException
from app.schemas.loan_schema import LoanCreate, ReturnRequest, LoanOut, ExtendRequest
from app.services import loan_service

router = APIRouter(prefix="/api/loans", tags=["Loans"])

@router.post("/", response_model=LoanOut)
def issue_book(loan: LoanCreate):
    return loan_service.issue_book(loan.dict())

@router.post("/return", response_model=LoanOut)
def return_book(req: ReturnRequest):
    return loan_service.return_book(req.loan_id)

@router.get("/{user_id}")
def user_loans(user_id: str):
    return loan_service.get_loans_by_user(user_id)

@router.get("/overdue")
def get_overdue():
    return loan_service.get_overdue_loans()

@router.put("/{loan_id}/extend", response_model=LoanOut)
def extend_loan(loan_id: str, req: ExtendRequest):
    loan = loan_service.extend_loan(loan_id, req.extension_days)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan