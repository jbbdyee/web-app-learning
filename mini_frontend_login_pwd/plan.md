# Supabase에서 로컬 PostgreSQL로 전환 계획

## 1. 목표

- 기존 `frontend`, `backend`는 수정하지 않고 유지한다.
- 기존 프로젝트를 복제해 `frontend_sql`, `backend_sql`을 만든다.
- `backend_sql`의 Supabase 테이블 CRUD를 로컬 PostgreSQL CRUD로 교체한다.
- 기존 화면, API 경로, 요청/응답 형식, 로그인 방식은 유지한다.
- 신규 구성은 기존 구성과 동시에 실행할 수 있도록 별도 포트를 사용한다.

## 2. 목표 폴더 구조

```text
mini_frontend_login_pwd/
├─ frontend/          # 기존 버전(보존)
├─ backend/           # 기존 Supabase 버전(보존)
├─ frontend_sql/      # backend_sql을 호출하는 신규 프론트엔드
├─ backend_sql/       # 로컬 PostgreSQL 연동 신규 백엔드
└─ plan.md
```

복제할 때 `.env`, `.venv`, `__pycache__`, `.pytest_cache`, `*.pyc`는 제외한다.

## 3. 실행 포트

| 구성 | 주소 |
|---|---|
| 기존 backend | `http://127.0.0.1:8000` |
| 신규 backend_sql | `http://127.0.0.1:8001` |
| 기존 frontend | `http://localhost:8501` |
| 신규 frontend_sql | `http://localhost:8502` |

## 4. backend_sql 전환

1. SQLAlchemy 2.x와 Psycopg 3을 의존성에 추가한다.
2. Supabase 패키지는 신규 백엔드 의존성에서 제거한다.
3. `DATABASE_URL` 환경변수를 읽는 `app/core/database.py`를 만든다.
4. `customers`, `products`용 SQLAlchemy 모델을 만든다.
5. `auth_service.py`, `product_service.py`의 Supabase 호출을 SQLAlchemy 처리로 교체한다.
6. 중복키, 연결 실패, 트랜잭션 실패를 적절한 HTTP 오류로 변환한다.
7. 기존 Router, Pydantic Schema, API 경로와 응답 형식은 유지한다.
8. Swagger 설명에 남아 있는 Supabase 표현을 PostgreSQL로 변경한다.

## 5. PostgreSQL 스키마

```text
customers
- id TEXT PRIMARY KEY
- pwd TEXT NOT NULL
- name TEXT NOT NULL

products
- id TEXT PRIMARY KEY
- name TEXT NOT NULL
- price INTEGER NOT NULL CHECK (price >= 0)
- created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
```

- `sql/schema.sql`: 테이블 생성 SQL
- `sql/seed.sql`: 중복 실행 가능한 상품 예제 데이터
- 기존 비밀번호 해시 및 검증 로직은 그대로 사용한다.

## 6. frontend_sql 전환

1. 기존 화면과 브라우저 세션 로그인 로직을 유지한다.
2. `BACKEND_API_URL` 환경변수로 백엔드 주소를 설정한다.
3. 기본 주소는 신규 백엔드인 `http://127.0.0.1:8001`로 설정한다.
4. 로그인, 회원가입, 마이페이지 API 계약은 변경하지 않는다.

## 7. 환경변수

`backend_sql/.env.example`:

```env
DATABASE_URL=postgresql+psycopg://agent_user:your_password@127.0.0.1:5433/agent_db
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash-lite
```

`frontend_sql/.env.example`:

```env
BACKEND_API_URL=http://127.0.0.1:8001
```

실제 비밀번호와 API 키가 담긴 `.env`는 Git에서 제외한다.

## 8. 테스트 및 검증

1. Python 구문 컴파일 검사를 수행한다.
2. 기존 Router 테스트가 신규 서비스 구조에서도 통과하는지 확인한다.
3. DB 연결 실패 시 민감정보가 노출되지 않는지 확인한다.
4. 로컬 PostgreSQL을 사용할 수 있으면 다음 통합 테스트를 수행한다.
   - 회원가입 및 중복 ID 409
   - 로그인 성공 및 실패 401
   - 마이페이지 조회·수정
   - 상품 생성·조회·수정·삭제
5. `frontend_sql → backend_sql → PostgreSQL` 전체 흐름을 확인한다.

## 9. 실행 순서

1. Docker Desktop에서 `aidevs-pgvector` 컨테이너가 실행 중인지 확인한다.
2. 호스트 `127.0.0.1:5433`으로 `agent_db`에 연결한 뒤 `backend_sql/sql/schema.sql`, `seed.sql`을 실행한다.
3. `backend_sql/.env.example`을 참고하여 `.env`를 만든다.
4. backend_sql 의존성을 설치하고 8001 포트로 실행한다.
5. frontend_sql 의존성을 설치하고 8502 포트로 실행한다.
6. Swagger와 Streamlit 화면에서 전체 기능을 확인한다.

## 10. 완료 기준

- 기존 `frontend`, `backend`가 보존되어 있다.
- 신규 폴더 두 개가 독립적으로 실행 가능하다.
- `backend_sql` 코드에 Supabase 런타임 의존성이 없다.
- 기존 API 계약을 유지하면서 로컬 PostgreSQL에 데이터가 저장된다.
- 설치, DB 초기화, 환경변수, 실행 방법이 README에 기록되어 있다.
