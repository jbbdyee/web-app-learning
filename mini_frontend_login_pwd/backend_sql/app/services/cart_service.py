from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.database import session_scope
from app.models.cart import Cart
from app.models.customer import Customer
from app.models.product import Product
from app.schemas.cart_schema import CartCreate, CartPublic, CartUpdate


def cart_create(cart: CartCreate) -> CartPublic:
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    db_cart = Cart(
        id=now.strftime("%Y%m%d%H%M%S"),
        user_id=cart.user_id,
        item_id=cart.item_id,
        count=cart.count,
        created_date=now,
    )

    try:
        with session_scope() as session:
            if session.get(Customer, cart.user_id) is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"사용자 ID {cart.user_id}를 찾을 수 없습니다.",
                )
            if session.get(Product, cart.item_id) is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"상품 ID {cart.item_id}를 찾을 수 없습니다.",
                )
            session.add(db_cart)
            session.flush()
            return _to_public(db_cart)
    except IntegrityError as error:
        raise HTTPException(
            status_code=409,
            detail="같은 초에 생성된 장바구니 ID가 이미 존재합니다. 다시 시도해 주세요.",
        ) from error
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def cart_get_all() -> list[CartPublic]:
    try:
        with session_scope() as session:
            carts = session.scalars(
                select(Cart).order_by(Cart.created_date.desc())
            ).all()
            return [_to_public(cart) for cart in carts]
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def cart_get(cart_id: str) -> CartPublic | None:
    try:
        with session_scope() as session:
            cart = session.get(Cart, cart_id)
            return None if cart is None else _to_public(cart)
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def cart_get_by_user(user_id: str) -> list[CartPublic]:
    try:
        with session_scope() as session:
            if session.get(Customer, user_id) is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"사용자 ID {user_id}를 찾을 수 없습니다.",
                )
            carts = session.scalars(
                select(Cart)
                .where(Cart.user_id == user_id)
                .order_by(Cart.created_date.desc())
            ).all()
            return [_to_public(cart) for cart in carts]
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def cart_update(cart_id: str, cart: CartUpdate) -> CartPublic | None:
    try:
        with session_scope() as session:
            db_cart = session.get(Cart, cart_id)
            if db_cart is None:
                return None
            db_cart.count = cart.count
            session.flush()
            return _to_public(db_cart)
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def cart_delete(cart_id: str) -> CartPublic | None:
    try:
        with session_scope() as session:
            cart = session.get(Cart, cart_id)
            if cart is None:
                return None
            result = _to_public(cart)
            session.delete(cart)
            return result
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def _to_public(cart: Cart) -> CartPublic:
    return CartPublic(
        id=cart.id,
        user_id=cart.user_id,
        item_id=cart.item_id,
        count=cart.count,
        created_date=cart.created_date,
    )
