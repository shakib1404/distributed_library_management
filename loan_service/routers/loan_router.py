from fastapi import APIRouter, HTTPException
from schemas.loan_schema import LoanCreate, ReturnRequest, LoanOut, LoanWithBook, LoanDetails
from services.loan_service import LoanService

router = APIRouter(prefix="/api/loans", tags=["Loans"])
loan_service = LoanService()

@router.post("/", response_model=LoanOut)
async def issue_book(loan: LoanCreate):
    return await loan_service.issue_book(loan)

@router.post("/returns", response_model=LoanOut)
async def return_book(req: ReturnRequest):
    return await loan_service.return_book(req.loan_id)

@router.get("/user/{user_id}")
async def get_user_loans(user_id: str):
    return await loan_service.get_loans_by_user(user_id)

@router.get("/{loan_id}", response_model=LoanDetails)
async def get_loan(loan_id: str):
    loan = await loan_service.get_loan_by_id(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    return loan