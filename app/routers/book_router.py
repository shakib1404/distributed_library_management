from fastapi import APIRouter, HTTPException
from app.schemas.book_schema import BookCreate, BookUpdate, BookOut
from app.services import book_service

router = APIRouter(prefix="/api/books", tags=["Books"])

@router.post("/", response_model=BookOut)
def add_book(book: BookCreate):
    book_id = book_service.create_book(book.dict())
    return {**book.dict(), "id": book_id, "available_copies": book.copies}

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: str):
    book = book_service.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: str, book: BookUpdate):
    return book_service.update_book(book_id, book.dict(exclude_unset=True))

@router.delete("/{book_id}")
def delete_book(book_id: str):
    book_service.delete_book(book_id)
    return {"message": "Book deleted"}

@router.get("/")
def search_books(search: str):
    return book_service.search_books(search)
