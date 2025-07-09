import httpx
from database import db
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException


class LoanService:
    def __init__(self):
        self.user_service_url = "https://172.18.0.1/api//users"
        self.book_service_url = "https://172.18.0.1/api/books"

    async def issue_book(self, loan_data):
        async with httpx.AsyncClient(verify=False) as client:
            user_resp = await client.get(f"{self.user_service_url}/{loan_data.user_id}")
            if user_resp.status_code != 200:
                raise HTTPException(status_code=404, detail="User not found")

            book_resp = await client.get(f"{self.book_service_url}/{loan_data.book_id}")
            if book_resp.status_code != 200:
                raise HTTPException(status_code=404, detail="Book not found")

            book = book_resp.json()
            if book["available_copies"] <= 0:
                raise HTTPException(status_code=400, detail="Book not available")

            patch_resp = await client.patch(
                f"{self.book_service_url}/{loan_data.book_id}/availability",
                json={"operation": "decrement"}
            )
            if patch_resp.status_code != 200:
                raise HTTPException(status_code=503, detail="Failed to update book availability")

        loan_doc = loan_data.dict()
        loan_doc["issue_date"] = datetime.utcnow()
        loan_doc["status"] = "ACTIVE"
        loan_doc["extensions_count"] = 0

        result = db.loans.insert_one(loan_doc)
        loan_doc["id"] = str(result.inserted_id)
        return loan_doc

    async def return_book(self, loan_id):
        db.loans.update_one(
            {"_id": ObjectId(loan_id)},
            {"$set": {"status": "RETURNED", "return_date": datetime.utcnow()}}
        )

        loan = db.loans.find_one({"_id": ObjectId(loan_id)})
        book_id = loan["book_id"]

        async with httpx.AsyncClient(verify=False) as client:
            patch_resp = await client.patch(
                f"{self.book_service_url}/{book_id}/availability",
                json={"operation": "increment"}
            )
            if patch_resp.status_code != 200:
                raise HTTPException(status_code=503, detail="Failed to update book availability")

        loan["id"] = str(loan["_id"])
        return loan

    def get_loans_by_user(self, user_id):
        cursor = db.loans.find({"user_id": user_id})
        result = []

        async def build_result():
            async with httpx.AsyncClient(verify=False) as client:
                for loan in cursor:
                    try:
                        book_resp = await client.get(f"{self.book_service_url}/{loan['book_id']}")
                        book = book_resp.json()
                    except Exception:
                        continue

                    result.append({
                        "id": str(loan["_id"]),
                        "book": {
                            "id": book["id"],
                            "title": book["title"],
                            "author": book["author"]
                        },
                        "issue_date": loan["issue_date"],
                        "due_date": loan["due_date"],
                        "return_date": loan.get("return_date"),
                        "status": loan["status"]
                    })

            return {"loans": result, "total": len(result)}

        return build_result()

    async def get_loan_by_id(self, loan_id):
        loan = db.loans.find_one({"_id": ObjectId(loan_id)})
        if not loan:
            return None

        async with httpx.AsyncClient(verify=False) as client:
            user_resp = await client.get(f"{self.user_service_url}/{loan['user_id']}")
            book_resp = await client.get(f"{self.book_service_url}/{loan['book_id']}")

            if user_resp.status_code != 200 or book_resp.status_code != 200:
                raise HTTPException(status_code=503, detail="Failed to fetch user or book")

        return {
            "id": str(loan["_id"]),
            "user": user_resp.json(),
            "book": book_resp.json(),
            "issue_date": loan["issue_date"],
            "due_date": loan["due_date"],
            "return_date": loan.get("return_date"),
            "status": loan["status"]
        }
