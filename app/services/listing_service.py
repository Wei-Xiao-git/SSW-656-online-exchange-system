from app.database.database import SessionLocal
from app.database.listing_model import ListingDB
from app.database.user_model import UserDB


def create_listing(listing, seller_id: int):
    db = SessionLocal()

    seller = db.query(UserDB).filter(
        UserDB.id == seller_id
    ).first()

    if not seller:
        db.close()
        raise ValueError("Seller not found")

    new_listing = ListingDB(
        title=listing.title,
        description=listing.description,
        price=listing.price,
        seller_id=seller_id
    )

    db.add(new_listing)
    db.commit()
    db.close()

    return {"message": "Listing created successfully"}


def get_all_listings():
    db = SessionLocal()
    listings = db.query(ListingDB).all()
    db.close()
    return listings


def search_listings(keyword: str):
    db = SessionLocal()

    results = db.query(ListingDB).filter(
        ListingDB.title.contains(keyword)
    ).all()

    db.close()

    return results