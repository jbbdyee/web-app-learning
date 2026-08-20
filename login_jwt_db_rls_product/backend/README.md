# Supabase Auth + Product RLS 백엔드

Supabase Auth로 로그인하고, PostgreSQL RLS를 적용한 Product CRUD를 호출하는 FastAPI 예제입니다.

`shop.users.role`을 기준으로 권한을 나눕니다.

- 일반 사용자(`user`): 상품 조회만 가능
- 관리자(`admin`): 상품 조회·생성·수정·삭제 가능

FastAPI가 관리자 쓰기 요청을 검사하고, Supabase의 `products` RLS 정책도 같은 권한을 최종적으로 검사합니다.

## 실행

1. [DB_GUIDE.md](DB_GUIDE.md)에 따라 Supabase Dashboard를 설정합니다.
2. `.env.example`을 `.env`로 복사하고 실제 값을 입력합니다.
3. 백엔드를 실행합니다.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API 문서는 `http://127.0.0.1:8000/docs`에서 확인합니다.
