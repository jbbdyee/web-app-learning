from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.core.database import session_scope
from app.core.password import hash_password, verify_password
from app.models.customer import Customer
from app.schemas.auth_scheme import AuthCreate, AuthLogin, AuthPublic, AuthUpdate


def sign_up_process(auth: AuthCreate) -> AuthPublic:
    try:
        with session_scope() as session:
            if session.get(Customer, auth.id) is not None:
                raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다.")
            customer = Customer(id=auth.id, pwd=hash_password(auth.pwd), name=auth.name)
            session.add(customer)
            session.flush()
            return _to_public(customer)
    except IntegrityError as error:
        raise HTTPException(status_code=409, detail="이미 사용 중인 아이디입니다.") from error
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def update_process(auth: AuthUpdate) -> AuthPublic:
    try:
        with session_scope() as session:
            customer = session.get(Customer, auth.id)
            if customer is None:
                raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
            customer.pwd = hash_password(auth.pwd)
            customer.name = auth.name
            session.flush()
            return _to_public(customer)
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def sign_in_process(auth: AuthLogin) -> AuthPublic:
    customer = _customer_get(auth.id)
    if customer is None or not verify_password(auth.pwd, customer.pwd):
        raise HTTPException(status_code=401, detail="아이디 또는 비밀번호가 올바르지 않습니다.")
    return _to_public(customer)


def sign_out_process(input_id: str) -> AuthPublic:
    return AuthPublic(id=input_id)


def my_page_process(input_id: str) -> AuthPublic:
    customer = _customer_get(input_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    return _to_public(customer)


def _customer_get(customer_id: str) -> Customer | None:
    try:
        with session_scope() as session:
            return session.scalar(select(Customer).where(Customer.id == customer_id))
    except (RuntimeError, SQLAlchemyError) as error:
        raise HTTPException(status_code=500, detail="DB 처리에 실패했습니다.") from error


def _to_public(customer: Customer) -> AuthPublic:
    return AuthPublic(id=customer.id, name=customer.name)
