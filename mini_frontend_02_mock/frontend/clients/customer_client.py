# customer_client.py
# customer CRUD

from typing import Any
from core.api_client import request

def customer_insert(customer: dict):
     return request("POST",f"/customer/create", json=customer)

def customer_delete(customer_id: int):
    return request("DELETE",f"/customer/delete/{customer_id}")

def customer_update(customer_id: int, customer: dict):
    return request("PUT",f"/customer/update/{customer_id}", json=customer)

def customer_select_all():
    return request("GET",f"/customer/getall")

def customer_select(customer_id: int):
    return request("GET",f"/customer/get/{customer_id}")