from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import create_client

from app.core.db_config import (
    SUPABASE_PUBLISHABLE_KEY,
    SUPABASE_URL,
    check_db_config,
)
from app.schemes.auth_scheme import CurrentUser
from app.services.user_service import get_user_profile


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> CurrentUser:
    """Supabase Auth 토큰을 검증합니다."""

    if credentials is None:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    token = credentials.credentials

    try:
        check_db_config()
        auth_client = create_client(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY)
        auth_response = auth_client.auth.get_user(token)
        user = auth_response.user

        if user is None:
            raise HTTPException(status_code=401, detail="사용자를 확인할 수 없습니다.")

        _, role = get_user_profile(token, str(user.id))

        return CurrentUser(
            user_id=str(user.id),
            email=user.email or "",
            role=role,
            access_token=token,
        )
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail="토큰이 올바르지 않거나 만료되었습니다.",
        ) from error


def require_admin(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    """관리자 역할만 쓰기 작업을 수행하도록 제한합니다."""

    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="관리자 권한이 필요합니다.")
    return current_user
