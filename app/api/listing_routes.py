from fastapi import APIRouter, Depends
from app.models.listing import Listing
from app.services.listing_service import (
    create_listing,
    get_all_listings,
    search_listings
)
from fastapi import HTTPException
from app.security.auth_dependency import get_current_user

router = APIRouter()


@router.post("/listings")
def create_new_listing(
    listing: Listing,
    current_user=Depends(get_current_user)
):
    try:
        return create_listing(
            listing,
            seller_id=current_user["user_id"]
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/listings")
def list_all():
    return get_all_listings()


@router.get("/listings/search")
def search(keyword: str):
    return search_listings(keyword)