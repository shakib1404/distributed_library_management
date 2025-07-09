from fastapi import FastAPI
from routers.book_router import router

app = FastAPI(title="book service")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Book Service is running"}

