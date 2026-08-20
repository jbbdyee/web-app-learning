from datetime import datetime

from fastapi.testclient import TestClient

from app.main import app
from app.routers import cart_router
from app.schemas.cart_schema import CartPublic


client = TestClient(app)


def make_cart(cart_id: str = "20260814153027") -> CartPublic:
    return CartPublic(
        id=cart_id,
        user_id="id77",
        item_id="product-1",
        count=2,
        created_date=datetime.fromisoformat("2026-08-14T15:30:27+09:00"),
    )


def test_create_cart_returns_created_cart(monkeypatch):
    monkeypatch.setattr(cart_router, "cart_create", lambda cart: make_cart())

    response = client.post(
        "/cart/create",
        json={"user_id": "id77", "item_id": "product-1", "count": 2},
    )

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["id"] == "20260814153027"


def test_get_all_carts_returns_list(monkeypatch):
    monkeypatch.setattr(cart_router, "cart_get_all", lambda: [make_cart()])

    response = client.get("/cart/getall")

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_get_cart_returns_404_when_missing(monkeypatch):
    monkeypatch.setattr(cart_router, "cart_get", lambda cart_id: None)

    response = client.get("/cart/get/missing-cart")

    assert response.status_code == 404


def test_get_carts_by_user(monkeypatch):
    monkeypatch.setattr(
        cart_router,
        "cart_get_by_user",
        lambda user_id: [make_cart()],
    )

    response = client.get("/cart/user/id77")

    assert response.status_code == 200
    assert response.json()["data"][0]["user_id"] == "id77"


def test_update_cart_count(monkeypatch):
    received = {}

    def fake_update(cart_id, cart):
        received["cart_id"] = cart_id
        received["count"] = cart.count
        updated = make_cart(cart_id)
        updated.count = cart.count
        return updated

    monkeypatch.setattr(cart_router, "cart_update", fake_update)

    response = client.put("/cart/20260814153027", json={"count": 5})

    assert response.status_code == 200
    assert response.json()["data"]["count"] == 5
    assert received == {"cart_id": "20260814153027", "count": 5}


def test_delete_cart(monkeypatch):
    monkeypatch.setattr(
        cart_router,
        "cart_delete",
        lambda cart_id: make_cart(cart_id),
    )

    response = client.delete("/cart/delete/20260814153027")

    assert response.status_code == 200
    assert response.json()["data"]["id"] == "20260814153027"


def test_create_cart_rejects_zero_count():
    response = client.post(
        "/cart/create",
        json={"user_id": "id77", "item_id": "product-1", "count": 0},
    )

    assert response.status_code == 422
