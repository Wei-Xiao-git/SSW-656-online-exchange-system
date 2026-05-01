from fastapi import APIRouter
from app.models.listing import Listing
from app.services.listing_service import (
    create_listing,
    get_all_listings,
    search_listings
)
from fastapi import HTTPException

router = APIRouter()


@router.post("/listings")
def create_new_listing(listing: Listing):
    try:
        return create_listing(listing)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/listings")
def list_all():
    return get_all_listings()


@router.get("/listings/search")
def search(keyword: str):
    return search_listings(keyword)