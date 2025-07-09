from fastapi import FastAPI
from routers.user_router import router

app = FastAPI(title="User Service")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "User Service is running"}

