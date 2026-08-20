# backend_sql

기존 FastAPI API 계약을 유지하면서 Supabase 대신 로컬 PostgreSQL을 사용하는 백엔드입니다.

## 1. PostgreSQL 준비

Docker Desktop의 `aidevs-pgvector` 컨테이너를 사용합니다.

```text
호스트 접속 주소: 127.0.0.1:5433
컨테이너 내부 포트: 5432
데이터베이스: agent_db
사용자: agent_user
```

데이터베이스에 접속해 다음 파일을 순서대로 실행합니다. 로컬에 `psql`이 없다면 애플리케이션의 SQLAlchemy/Psycopg 연결로 적용할 수 있습니다.

```powershell
psql -h 127.0.0.1 -p 5433 -U agent_user -d agent_db -f sql/schema.sql
psql -h 127.0.0.1 -p 5433 -U agent_user -d agent_db -f sql/seed.sql
```

`seed.sql`은 `ON CONFLICT DO NOTHING`을 사용하므로 다시 실행해도 상품 ID가 중복되지 않습니다.

## 2. 환경변수

`.env.example`을 복사해 `.env`를 만들고 실제 PostgreSQL 비밀번호를 입력합니다.

```env
DATABASE_URL=postgresql+psycopg://agent_user:your_password@127.0.0.1:5433/agent_db
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash-lite
```

특수문자가 포함된 사용자명이나 비밀번호는 URL 인코딩해야 합니다. 실제 `.env`는 Git에 포함하지 않습니다.

## 3. 설치 및 실행

```powershell
cd backend_sql
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8001
```

- Swagger: `http://127.0.0.1:8001/docs`
- 테스트: `python -m pytest`
- 실제 PostgreSQL CRUD 검증: `python -m scripts.verify_postgres`

## 4. 주요 구조

```text
app/
├─ core/database.py       # DATABASE_URL, engine, session, transaction
├─ models/customer.py     # customers ORM 모델
├─ models/product.py      # products ORM 모델
├─ routers/               # 기존 API 경로 유지
├─ schemas/               # 기존 요청·응답 모델 유지
└─ services/              # SQLAlchemy 기반 CRUD
sql/
├─ schema.sql
└─ seed.sql
```

회원 비밀번호는 기존과 동일하게 PBKDF2 해시로 저장되며 API 응답에 포함되지 않습니다.

## 5. Cart API

장바구니는 `customers.id`와 `products.id`를 외래키로 참조합니다. `count`는 1 이상이어야 하며 `id`는 생성 시각의 `년월일시분초` 14자리로 생성됩니다.

| 기능 | 메서드 | 경로 |
|---|---|---|
| 등록 | POST | `/cart/create` |
| 전체 조회 | GET | `/cart/getall` |
| 단건 조회 | GET | `/cart/get/{cart_id}` |
| 사용자별 조회 | GET | `/cart/user/{user_id}` |
| 수량 수정 | PUT | `/cart/{cart_id}` |
| 삭제 | DELETE | `/cart/delete/{cart_id}` |

Swagger `http://127.0.0.1:8001/docs`의 `Cart` 그룹에서 순서대로 테스트할 수 있습니다.
