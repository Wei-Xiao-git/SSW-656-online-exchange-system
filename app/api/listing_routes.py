from fastapi import APIRouter
from app.models.listing import Listing
from app.services.listing_service import (
    create_listing,
    get_all_listings,
    search_listings
)

router = APIRouter()


@router.post("/listings")
def create_new_listing(listing: Listing):
    return create_listing(listing)


@router.get("/listings")
def list_all():
    return get_all_listings()


@router.get("/listings/search")
def search(keyword: str):
    return search_listings(keyword)