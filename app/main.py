from fastapi import FastAPI
from app.database.database import Base, engine
from app.database import (
    user_model,
    listing_model,
    order_model
)

from app.api.auth_routes import router as auth_router
from app.api.listing_routes import router as listing_router
from app.api.order_routes import router as order_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Online Exchange System API")

app.include_router(auth_router)
app.include_router(listing_router)
app.include_router(order_router)
