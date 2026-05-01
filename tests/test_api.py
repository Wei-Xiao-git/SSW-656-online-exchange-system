from fastapi.testclient import TestClient
from app.main import app

from app.database.database import SessionLocal
from app.database.user_model import UserDB
from app.database.listing_model import ListingDB
from app.database.order_model import OrderDB

import pytest

client = TestClient(app)


# -----------------------------
# Reset DB Before Each Test
# -----------------------------
@pytest.fixture(autouse=True)
def clean_database():
    db = SessionLocal()

    db.query(OrderDB).delete()
    db.query(ListingDB).delete()
    db.query(UserDB).delete()

    db.commit()
    db.close()


# -----------------------------
# Helper Functions
# -----------------------------
def register_user(username, email):
    return client.post("/register", json={
        "username": username,
        "password": "123456",
        "email": email
    })


def login_user(username):
    response = client.post("/login", json={
        "username": username,
        "password": "123456"
    })

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


# -----------------------------
# Auth Tests
# -----------------------------
def test_register_user():
    response = register_user("alice", "alice@example.com")

    assert response.status_code == 200


def test_login_returns_token():
    register_user("alice", "alice@example.com")

    response = client.post("/login", json={
        "username": "alice",
        "password": "123456"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()


# -----------------------------
# Listing Tests
# -----------------------------
def test_create_listing_authenticated():
    register_user("seller1", "seller@example.com")

    headers = login_user("seller1")

    response = client.post(
        "/listings",
        headers=headers,
        json={
            "title": "MacBook Air",
            "description": "Used laptop",
            "price": 800
        }
    )

    assert response.status_code == 200


def test_create_listing_unauthorized():
    response = client.post(
        "/listings",
        json={
            "title": "MacBook Air",
            "description": "Used laptop",
            "price": 800
        }
    )

    assert response.status_code == 403 or response.status_code == 401


# -----------------------------
# Order Tests
# -----------------------------
def test_create_order_authenticated():
    # Seller creates listing
    register_user("seller1", "seller@example.com")
    seller_headers = login_user("seller1")

    client.post(
        "/listings",
        headers=seller_headers,
        json={
            "title": "MacBook Air",
            "description": "Used laptop",
            "price": 800
        }
    )

    # Buyer places order
    register_user("buyer1", "buyer@example.com")
    buyer_headers = login_user("buyer1")

    response = client.post(
        "/orders",
        headers=buyer_headers,
        json={
            "listing_id": 1,
            "quantity": 1,
            "status": "Pending"
        }
    )

    assert response.status_code == 200


def test_create_order_unauthorized():
    response = client.post(
        "/orders",
        json={
            "listing_id": 1,
            "quantity": 1,
            "status": "Pending"
        }
    )

    assert response.status_code == 403 or response.status_code == 401


# -----------------------------
# Cancel Order Test
# -----------------------------
def test_cancel_order_authenticated():
    register_user("seller1", "seller@example.com")
    seller_headers = login_user("seller1")

    client.post(
        "/listings",
        headers=seller_headers,
        json={
            "title": "MacBook Air",
            "description": "Used laptop",
            "price": 800
        }
    )

    register_user("buyer1", "buyer@example.com")
    buyer_headers = login_user("buyer1")

    client.post(
        "/orders",
        headers=buyer_headers,
        json={
            "listing_id": 1,
            "quantity": 1,
            "status": "Pending"
        }
    )

    response = client.delete(
        "/orders/1",
        headers=buyer_headers
    )

    assert response.status_code == 200