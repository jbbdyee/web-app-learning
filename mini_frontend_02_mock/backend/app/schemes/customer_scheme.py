#  customer_scheme.py
from pydantic import BaseModel, Field

class CustomerCreate(BaseModel):
    id: int
    pwd: str
    name: str
    age: int

class CustomerUpdate(BaseModel):
    name: str
    age: int

class CustomerResponse(BaseModel):
    id: int
    name: str
    age: int


