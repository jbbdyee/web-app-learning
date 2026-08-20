from app.services import product_service
from fastapi import HTTPException
import pytest


class FakeResponse:
    status_code = 200
    is_error = False
    content = b'[{"id":1,"name":"T-shirt","price":15000}]'

    def json(self):
        return [{"id": 1, "name": "T-shirt", "price": 15000}]


def test_product_request_uses_user_token_not_service_role(monkeypatch):
    monkeypatch.setattr(product_service, "check_db_config", lambda: None)
    monkeypatch.setattr(product_service, "SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setattr(product_service, "SUPABASE_PUBLISHABLE_KEY", "publishable-key")

    def fake_request(method, url, params, json, headers, timeout):
        assert headers["apikey"] == "publishable-key"
        assert headers["Authorization"] == "Bearer user-access-token"
        assert headers["Accept-Profile"] == "shop"
        assert headers["Content-Profile"] == "shop"
        assert "service" not in headers["Authorization"]
        return FakeResponse()

    monkeypatch.setattr(product_service.httpx, "request", fake_request)

    rows = product_service.request_products("GET", "user-access-token")

    assert rows[0]["name"] == "T-shirt"


def test_product_request_exposes_supabase_error_message(monkeypatch):
    monkeypatch.setattr(product_service, "check_db_config", lambda: None)
    monkeypatch.setattr(product_service, "SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setattr(product_service, "SUPABASE_PUBLISHABLE_KEY", "publishable-key")

    class ErrorResponse:
        status_code = 400
        is_error = True
        content = b'{"message":"Could not find the table shop.products"}'
        text = 'Could not find the table shop.products'

        def json(self):
            return {"message": "Could not find the table shop.products"}

    monkeypatch.setattr(
        product_service.httpx,
        "request",
        lambda *args, **kwargs: ErrorResponse(),
    )

    with pytest.raises(HTTPException) as caught:
        product_service.request_products("POST", "user-access-token", json={})

    assert caught.value.status_code == 502
    assert "Could not find the table shop.products" in caught.value.detail
