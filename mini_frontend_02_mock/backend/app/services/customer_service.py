#  customer_service.py
from app.schemes.customer_scheme import CustomerCreate, CustomerResponse, CustomerUpdate
from zoneinfo import ZoneInfo
from datetime import datetime

# 1. 입력
def customer_create(customer: CustomerCreate) -> CustomerResponse | None:
    # Database 에 입력
    return CustomerResponse(
        id = customer.id,
        pwd = customer.pwd,
        name = customer.name,
        age = customer.age
    )

# 2. 전체조회
def customer_get_all() -> list[CustomerResponse]:
    list = []
    list.append(CustomerResponse(
        id = 100,
        name = "다영",
        age = 21
    ))
    list.append(CustomerResponse(
        id = 101,
        name = "다일",
        age = 31
    ))
    list.append(CustomerResponse(
        id = 103,
        name = "다이",
        age = 41
    ))
    list.append(CustomerResponse(
        id = 104,
        name = "다삼",
        age = 51
    ))
    return list 

# 3. 한개조회
def customer_get(customer_id: str) -> CustomerResponse | None:

    return CustomerResponse(
        id = customer_id,
        name = "다영",
        age = 21
    )

# 4. 삭제
def customer_delete(customer_id: int) -> CustomerResponse | None:

    return CustomerResponse(
        id = customer_id,
        name = "삭제된다영",
        age = 21
    )
# 5. 수정
def customer_update(customer_id, customer: CustomerUpdate) -> CustomerResponse | None:

    return CustomerResponse(
        id = customer_id,
        name = "수정된다영",
        age = 21
    )