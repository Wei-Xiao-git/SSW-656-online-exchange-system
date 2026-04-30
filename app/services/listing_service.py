from app.database.database import fake_listings_db


def create_listing(listing):
    fake_listings_db.append(listing)
    return {"message": "Listing created successfully"}


def get_all_listings():
    return fake_listings_db


def search_listings(keyword: str):
    results = []

    for listing in fake_listings_db:
        if keyword.lower() in listing.title.lower():
            results.append(listing)

    return results