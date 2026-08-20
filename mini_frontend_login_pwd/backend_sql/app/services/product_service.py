from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.database import session_scope
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductPublic, ProductUpdate


def product_create(product: ProductCreate) -> ProductPublic | None:
    now = datetime.now(ZoneInfo("Asia/Seoul"))
    db_product = Product(
        id=now.strftime("%Y%m%d%H%M%S%f"),
        name=product.name,
        price=product.price,
        created_at=now,
    )
    try:
        with session_scope() as session:
            session.add(db_product)
            session.flush()
            return _to_public(db_product)
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def product_get_all() -> list[ProductPublic]:
    try:
        with session_scope() as session:
            products = session.scalars(select(Product).order_by(Product.created_at)).all()
            return [_to_public(product) for product in products]
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def product_get(product_id: str) -> ProductPublic | None:
    try:
        with session_scope() as session:
            product = session.get(Product, product_id)
            return None if product is None else _to_public(product)
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def product_delete(product_id: str) -> ProductPublic | None:
    try:
        with session_scope() as session:
            product = session.get(Product, product_id)
            if product is None:
                return None
            result = _to_public(product)
            session.delete(product)
            return result
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def product_update(product_id: str, product: ProductUpdate) -> ProductPublic | None:
    try:
        with session_scope() as session:
            db_product = session.get(Product, product_id)
            if db_product is None:
                return None
            db_product.name = product.name
            db_product.price = product.price
            session.flush()
            return _to_public(db_product)
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def _to_public(product: Product) -> ProductPublic:
    return ProductPublic(
        id=product.id,
        name=product.name,
        price=product.price,
        created_at=product.created_at,
    )
