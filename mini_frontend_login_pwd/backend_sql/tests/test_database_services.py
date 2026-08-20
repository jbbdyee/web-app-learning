import pytest
from fastapi import HTTPException

from app.core.database import Base, get_engine
from app.schemas.auth_scheme import AuthCreate, AuthLogin
from app.schemas.cart_schema import CartCreate, CartUpdate
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services.auth_service import sign_in_process, sign_up_process
from app.services.cart_service import (
    cart_create,
    cart_delete,
    cart_get,
    cart_get_all,
    cart_get_by_user,
    cart_update,
)
from app.services.product_service import (
    product_create,
    product_delete,
    product_get,
    product_get_all,
    product_update,
)


@pytest.fixture(autouse=True)
def isolated_database(monkeypatch, tmp_path):
    database_path = (tmp_path / "test.db").as_posix()
    monkeypatch.setenv("DATABASE_URL", f"sqlite+pysqlite:///{database_path}")
    get_engine.cache_clear()
    Base.metadata.create_all(get_engine())
    yield
    get_engine().dispose()
    get_engine.cache_clear()


def test_auth_service_signup_login_and_duplicate():
    created = sign_up_process(AuthCreate(id="tester", pwd="secret", name="테스터"))
    assert created.id == "tester"
    assert created.name == "테스터"
    assert sign_in_process(AuthLogin(id="tester", pwd="secret")).id == "tester"

    with pytest.raises(HTTPException) as duplicate:
        sign_up_process(AuthCreate(id="tester", pwd="other", name="중복"))
    assert duplicate.value.status_code == 409

    with pytest.raises(HTTPException) as invalid_login:
        sign_in_process(AuthLogin(id="tester", pwd="wrong"))
    assert invalid_login.value.status_code == 401


def test_product_service_crud():
    created = product_create(ProductCreate(name="바지", price=10000))
    assert created is not None
    assert product_get(created.id).name == "바지"
    assert len(product_get_all()) == 1

    updated = product_update(
        created.id,
        ProductUpdate(name="청바지", price=20000),
    )
    assert updated is not None
    assert updated.name == "청바지"
    assert updated.price == 20000

    deleted = product_delete(created.id)
    assert deleted is not None
    assert product_get(created.id) is None


def test_cart_service_crud():
    customer = sign_up_process(
        AuthCreate(id="cart-user", pwd="secret", name="장바구니 사용자")
    )
    product = product_create(ProductCreate(name="장바구니 상품", price=3000))
    assert product is not None

    created = cart_create(
        CartCreate(user_id=customer.id, item_id=product.id, count=2)
    )
    assert len(created.id) == 14
    assert cart_get(created.id).count == 2
    assert len(cart_get_all()) == 1
    assert len(cart_get_by_user(customer.id)) == 1

    updated = cart_update(created.id, CartUpdate(count=5))
    assert updated is not None
    assert updated.count == 5

    deleted = cart_delete(created.id)
    assert deleted is not None
    assert cart_get(created.id) is None


def test_cart_create_rejects_missing_user_and_product():
    product = product_create(ProductCreate(name="검증 상품", price=3000))
    assert product is not None

    with pytest.raises(HTTPException) as missing_user:
        cart_create(
            CartCreate(user_id="missing-user", item_id=product.id, count=1)
        )
    assert missing_user.value.status_code == 404

    sign_up_process(AuthCreate(id="cart-user", pwd="secret", name="사용자"))
    with pytest.raises(HTTPException) as missing_product:
        cart_create(
            CartCreate(user_id="cart-user", item_id="missing-product", count=1)
        )
    assert missing_product.value.status_code == 404
