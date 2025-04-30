from fastapi import FastAPI
from app.routers import user_router
from app.routers import book_router,loan_router,stats_router

app = FastAPI(title="Smart Library System")

# Register the user routes
app.include_router(user_router.router)
app.include_router(book_router.router)
app.include_router(loan_router.router)
app.include_router(stats_router.router)

# Optional: Health check
@app.get("/")
def root():
    return {"message": "Smart Library System is running"}
