from fastapi import APIRouter, HTTPException

from app.core.api_response import ApiResponse
from app.schemas.cart_schema import CartCreate, CartUpdate
from app.services.cart_service import (
    cart_create,
    cart_delete,
    cart_get,
    cart_get_all,
    cart_get_by_user,
    cart_update,
)


cart_router = APIRouter(tags=["Cart"])


@cart_router.post("/cart/create")
def create(cart: CartCreate) -> ApiResponse:
    return ApiResponse(
        success=True,
        message="장바구니 상품이 등록되었습니다.",
        data=cart_create(cart),
    )


@cart_router.get("/cart/getall")
def get_all() -> ApiResponse:
    return ApiResponse(
        success=True,
        message="전체 장바구니 조회에 성공했습니다.",
        data=cart_get_all(),
    )


@cart_router.get("/cart/get/{cart_id}")
def get(cart_id: str) -> ApiResponse:
    cart = cart_get(cart_id)
    if cart is None:
        raise HTTPException(
            status_code=404,
            detail=f"장바구니 ID {cart_id}를 찾을 수 없습니다.",
        )
    return ApiResponse(
        success=True,
        message="장바구니 조회에 성공했습니다.",
        data=cart,
    )


@cart_router.get("/cart/user/{user_id}")
def get_by_user(user_id: str) -> ApiResponse:
    return ApiResponse(
        success=True,
        message="사용자 장바구니 조회에 성공했습니다.",
        data=cart_get_by_user(user_id),
    )


@cart_router.put("/cart/{cart_id}")
def update(cart_id: str, cart: CartUpdate) -> ApiResponse:
    updated_cart = cart_update(cart_id, cart)
    if updated_cart is None:
        raise HTTPException(
            status_code=404,
            detail=f"장바구니 ID {cart_id}를 찾을 수 없습니다.",
        )
    return ApiResponse(
        success=True,
        message="장바구니 수량이 수정되었습니다.",
        data=updated_cart,
    )


@cart_router.delete("/cart/delete/{cart_id}")
def delete(cart_id: str) -> ApiResponse:
    deleted_cart = cart_delete(cart_id)
    if deleted_cart is None:
        raise HTTPException(
            status_code=404,
            detail=f"장바구니 ID {cart_id}를 찾을 수 없습니다.",
        )
    return ApiResponse(
        success=True,
        message="장바구니 상품이 삭제되었습니다.",
        data=deleted_cart,
    )
