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
def register_user(username, email, role):
    return client.post("/register", json={
        "username": username,
        "password": "123456",
        "email": email,
        "role": role
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
def test_register_with_role():
    response = register_user(
        "seller1",
        "seller@test.com",
        "seller"
    )

    assert response.status_code == 200


def test_login_returns_token():
    register_user("buyer1", "buyer@test.com", "buyer")

    response = client.post("/login", json={
        "username": "buyer1",
        "password": "123456"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()


# -----------------------------
# Listing RBAC Tests
# -----------------------------
def test_seller_can_create_listing():
    register_user("seller1", "seller@test.com", "seller")
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


def test_buyer_cannot_create_listing():
    register_user("buyer1", "buyer@test.com", "buyer")
    headers = login_user("buyer1")

    response = client.post(
        "/listings",
        headers=headers,
        json={
            "title": "MacBook Air",
            "description": "Used laptop",
            "price": 800
        }
    )

    assert response.status_code == 403


# -----------------------------
# Order RBAC Tests
# -----------------------------
def test_buyer_can_create_order():
    register_user("seller1", "seller@test.com", "seller")
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

    register_user("buyer1", "buyer@test.com", "buyer")
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


def test_seller_cannot_create_order():
    register_user("seller1", "seller@test.com", "seller")
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

    response = client.post(
        "/orders",
        headers=seller_headers,
        json={
            "listing_id": 1,
            "quantity": 1,
            "status": "Pending"
        }
    )

    assert response.status_code == 403


# -----------------------------
# Unauthorized Tests
# -----------------------------
def test_create_listing_without_token():
    response = client.post(
        "/listings",
        json={
            "title": "MacBook",
            "description": "Laptop",
            "price": 800
        }
    )

    assert response.status_code in [401, 403]


def test_create_order_without_token():
    response = client.post(
        "/orders",
        json={
            "listing_id": 1,
            "quantity": 1,
            "status": "Pending"
        }
    )

    assert response.status_code in [401, 403]