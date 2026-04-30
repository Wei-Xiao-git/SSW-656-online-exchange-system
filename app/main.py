from fastapi import FastAPI
from app.api.auth_routes import router as auth_router
from app.api.listing_routes import router as listing_router

app = FastAPI(title="Online Exchange System API")

app.include_router(auth_router)
app.include_router(listing_router)
