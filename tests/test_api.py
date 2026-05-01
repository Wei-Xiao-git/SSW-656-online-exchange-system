from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register():
    response = client.post("/register", json={
        "username": "alice",
        "password": "123456",
        "email": "alice@example.com"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


def test_create_listing():
    response = client.post("/listings", json={
        "title": "MacBook Air",
        "description": "Used laptop",
        "price": 800,
        "seller": "alice"
    })

    assert response.status_code == 200


def test_get_listings():
    response = client.get("/listings")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_order():
    response = client.post("/orders", json={
        "id": 1,
        "buyer": "bob",
        "listing_title": "MacBook Air",
        "quantity": 1,
        "status": "Pending"
    })

    assert response.status_code == 200