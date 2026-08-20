"""실제 PostgreSQL에서 서비스 CRUD를 검증하고 테스트 데이터를 정리합니다."""

from uuid import uuid4

from sqlalchemy import delete

from app.core.database import session_scope
from app.models.customer import Customer
from app.models.product import Product
from app.schemas.auth_scheme import AuthCreate, AuthLogin, AuthUpdate
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services.auth_service import (
    my_page_process,
    sign_in_process,
    sign_up_process,
    update_process,
)
from app.services.product_service import (
    product_create,
    product_delete,
    product_get,
    product_update,
)


def main() -> None:
    customer_id = f"codex_test_{uuid4().hex[:12]}"
    product_id: str | None = None

    try:
        created_customer = sign_up_process(
            AuthCreate(id=customer_id, pwd="temporary-secret", name="테스트")
        )
        assert created_customer.id == customer_id
        assert (
            sign_in_process(
                AuthLogin(id=customer_id, pwd="temporary-secret")
            ).id
            == customer_id
        )
        assert update_process(
            AuthUpdate(id=customer_id, pwd="changed-secret", name="수정됨")
        ).name == "수정됨"
        assert my_page_process(customer_id).name == "수정됨"

        created_product = product_create(
            ProductCreate(name="통합 테스트 상품", price=1000)
        )
        assert created_product is not None
        product_id = created_product.id
        found_product = product_get(product_id)
        assert found_product is not None
        assert found_product.name == "통합 테스트 상품"

        updated_product = product_update(
            product_id,
            ProductUpdate(name="수정 상품", price=2000),
        )
        assert updated_product is not None
        assert updated_product.price == 2000
        assert product_delete(product_id) is not None
        product_id = None
        print("PostgreSQL service CRUD: PASS")
    finally:
        with session_scope() as session:
            if product_id is not None:
                session.execute(delete(Product).where(Product.id == product_id))
            session.execute(delete(Customer).where(Customer.id == customer_id))


if __name__ == "__main__":
    main()
