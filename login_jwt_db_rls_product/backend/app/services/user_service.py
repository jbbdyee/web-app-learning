from typing import Literal

import httpx
from fastapi import HTTPException

from app.core.db_config import (
    SUPABASE_PUBLISHABLE_KEY,
    SUPABASE_URL,
    check_db_config,
)


def get_user_profile(
    access_token: str,
    user_id: str,
) -> tuple[str, Literal["user", "admin"]]:
    """현재 사용자의 이름과 역할을 RLS가 적용된 shop.users에서 조회합니다."""

    check_db_config()
    headers = {
        "apikey": SUPABASE_PUBLISHABLE_KEY,
        "Authorization": f"Bearer {access_token}",
        "Accept-Profile": "shop",
    }

    try:
        response = httpx.get(
            f"{SUPABASE_URL}/rest/v1/users",
            params={
                "select": "name,role",
                "user_id": f"eq.{user_id}",
                "limit": "1",
            },
            headers=headers,
            timeout=10.0,
        )
    except httpx.RequestError as error:
        raise HTTPException(
            status_code=503,
            detail="사용자 권한 정보를 조회할 수 없습니다.",
        ) from error

    if response.status_code in (401, 403):
        raise HTTPException(status_code=401, detail="로그인 세션이 유효하지 않습니다.")
    if response.is_error:
        raise HTTPException(status_code=503, detail="사용자 권한 정보를 조회할 수 없습니다.")

    rows = response.json()
    if not rows:
        raise HTTPException(status_code=403, detail="등록된 사용자 권한 정보가 없습니다.")

    role = rows[0].get("role")
    if role not in ("user", "admin"):
        raise HTTPException(status_code=403, detail="사용자 역할이 올바르지 않습니다.")

    return str(rows[0].get("name") or ""), role
