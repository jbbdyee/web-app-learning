#  customer_router.py

from fastapi import APIRouter
from app.schemes.customer_scheme import CustomerCreate, CustomerUpdate, CustomerResponse
from app.services.customer_service import (
    customer_get_all,
    customer_get,
    customer_create,
    customer_delete,
    customer_update,
)

customer_router = APIRouter(tags=["customer"])

@customer_router.post("/customer/create")
def create(customer:CustomerCreate) -> CustomerResponse:
    """customer 신규 입력"""
    return customer_create(customer)

@customer_router.get("/customer/get/{customer_id}")
def get(customer_id:int) -> CustomerResponse:
    return customer_get(customer_id)

@customer_router.get("/customer/getall")
def get_all() -> list[CustomerResponse]:
    return customer_get_all()

@customer_router.delete("/customer/delete/{customer_id}")
def delete(customer_id: int) -> CustomerResponse:
    return customer_delete(customer_id)

@customer_router.put("/customer/update/{customer_id}")
def update(customer_id: int, customer: CustomerUpdate) -> CustomerResponse:
    return customer_update(customer_id, customer)