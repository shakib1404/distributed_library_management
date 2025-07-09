from fastapi import FastAPI
from routers.loan_router import router

app = FastAPI(title="loan service")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Loan service is running"}

