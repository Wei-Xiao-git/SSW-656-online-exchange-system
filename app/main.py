from fastapi import FastAPI
from app.api.auth_routes import router as auth_router

app = FastAPI(title="Online Exchange System API")

app.include_router(auth_router)
