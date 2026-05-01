from fastapi.testclient import TestClient
from app.main import app

from app.database.database import SessionLocal
from app.database.user_model import UserDB
from app.database.listing_model import ListingDB
from app.database.order_model import OrderDB

import pytest

client = TestClient(app)


# ---------- Reset Database Before Each Test ----------

@pytest.fixture(autouse=True)
def clean_database():
    db = SessionLocal()

    db.query(OrderDB).delete()
    db.query(ListingDB).delete()
    db.query(UserDB).delete()

    db.commit()
    db.close()


# ---------- Auth Tests ----------

def test_register_user():
    response = client.post("/register", json={
        "username": "alice",
        "password": "123456",
        "email": "alice@example.com"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


def test_duplicate_user_registration():
    client.post("/register", json={
        "username": "alice",
        "password": "123456",
        "email": "alice@example.com"
    })

    response = client.post("/register", json={
        "username": "alice",
        "password": "abcdef",
        "email": "alice2@example.com"
    })

    assert response.status_code in [400, 409, 500]


# ---------- Listing Tests ----------

def test_create_listing():
    client.post("/register", json={
        "username": "seller1",
        "password": "123456",
        "email": "seller@example.com"
    })

    response = client.post("/listings", json={
        "title": "MacBook Air",
        "description": "Used laptop",
        "price": 800,
        "seller_id": 1
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Listing created successfully"


def test_create_listing_invalid_seller():
    response = client.post("/listings", json={
        "title": "iPhone",
        "description": "Phone",
        "price": 500,
        "seller_id": 999
    })

    assert response.status_code in [400, 404, 500]


def test_get_listings():
    client.post("/register", json={
        "username": "seller1",
        "password": "123456",
        "email": "seller@example.com"
    })

    client.post("/listings", json={
        "title": "MacBook Air",
        "description": "Used laptop",
        "price": 800,
        "seller_id": 1
    })

    response = client.get("/listings")

    assert response.status_code == 200
    assert len(response.json()) == 1


# ---------- Order Tests ----------

def test_create_order():
    # Seller
    client.post("/register", json={
        "username": "seller1",
        "password": "123456",
        "email": "seller@example.com"
    })

    # Buyer
    client.post("/register", json={
        "username": "buyer1",
        "password": "123456",
        "email": "buyer@example.com"
    })

    # Listing
    client.post("/listings", json={
        "title": "MacBook Air",
        "description": "Used laptop",
        "price": 800,
        "seller_id": 1
    })

    response = client.post("/orders", json={
        "buyer_id": 2,
        "listing_id": 1,
        "quantity": 1,
        "status": "Pending"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Order created successfully"


def test_create_order_invalid_buyer():
    response = client.post("/orders", json={
        "buyer_id": 999,
        "listing_id": 1,
        "quantity": 1,
        "status": "Pending"
    })

    assert response.status_code in [400, 404, 500]


def test_cancel_order():
    client.post("/register", json={
        "username": "seller1",
        "password": "123456",
        "email": "seller@example.com"
    })

    client.post("/register", json={
        "username": "buyer1",
        "password": "123456",
        "email": "buyer@example.com"
    })

    client.post("/listings", json={
        "title": "MacBook Air",
        "description": "Used laptop",
        "price": 800,
        "seller_id": 1
    })

    client.post("/orders", json={
        "buyer_id": 2,
        "listing_id": 1,
        "quantity": 1,
        "status": "Pending"
    })

    response = client.delete("/orders/1")

    assert response.status_code == 200