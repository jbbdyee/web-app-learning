from datetime import datetime

from pydantic import BaseModel, Field


class CartCreate(BaseModel):
    user_id: str = Field(min_length=1, examples=["id77"])
    item_id: str = Field(min_length=1, examples=["20260722090000000001"])
    count: int = Field(ge=1, examples=[2])


class CartUpdate(BaseModel):
    count: int = Field(ge=1, examples=[5])


class CartPublic(BaseModel):
    id: str = Field(examples=["20260814153027"])
    user_id: str
    item_id: str
    count: int
    created_date: datetime
