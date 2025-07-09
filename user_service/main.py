from fastapi import FastAPI
from fastapi import Request

from routers.user_router import router

app = FastAPI(title="User Service")
app.include_router(router)



@app.get("/")
def root():
    return {"message": "User Service is running"}

# Optional: log all incoming requests
@app.middleware("http")
async def trace_nginx_path(request: Request, call_next):
    print(f"📥 NGINX Routed: {request.method} {request.url.path}")
    return await call_next(request)
