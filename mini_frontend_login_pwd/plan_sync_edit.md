# 팀 프로젝트 개발 계획서 — Team01 통합 관리 서비스

## 1. 프로젝트 개요

### 1-1. 프로젝트명

```text
team01_0803 미니 프로젝트
```

### 1-2. 프로젝트 목표

> 스터디, 영화, 운동, 여행 정보를 체계적으로 관리하려는 사용자를 위해  
> 각 주제의 데이터를 생성·조회·수정·삭제할 수 있는 웹 서비스를 개발한다.

기존 프로젝트의 FastAPI 백엔드와 Streamlit 프론트엔드 구조를 활용하되 수업 예제인 `product` 기능은 제외한다.   
팀원 4명은 Frontend 2명, Backend 2명으로 역할을 나누고 각자의 이니셜 폴더에서 개발한다.

### 1-3. 주요 기능

- 스터디, 영화, 운동, 여행 정보 CRUD
- 각 데이터의 입력일시와 수정일시 자동 관리
- FastAPI와 Supabase 연동
- Streamlit 멀티페이지 관리 화면
- 회원가입, 로그인, 로그아웃, 회원정보 조회·수정
- 로그인 상태에 따른 Streamlit 페이지 접근 제어
- 입력값 검증 및 기본 예외 처리
- 하나의 Supabase 프로젝트를 이용한 4인 공동 개발

### 1-4. 구현 범위

#### 이번 프로젝트에 포함

- `studies`, `movies`, `exercises`, `travels` 테이블
- 테이블별 생성·목록 조회·단건 조회·수정·삭제
- `created_at`, `updated_at` 자동 기록
- 테이블별 FastAPI Router, Schema, Service
- 테이블별 Streamlit 관리 페이지
- Supabase 공통 연결 모듈
- `customers` 테이블 기반 인증 Router, Schema, Service
- 비밀번호 해시 저장 및 로그인 비밀번호 검증
- 로그인, 회원가입, 마이페이지 화면
- Swagger와 Streamlit을 이용한 테스트
- GitHub 브랜치 협업

---

## 2. 기능별 완료 기준

| 기능 | 담당자 | 완료 기준 |
|---|---|---|
| 스터디 관리 | `dn`·`tk` | 스터디 CRUD가 화면, API, Supabase에서 정상 동작한다. |
| 영화 관리 | `dn`·`tk` | 영화 CRUD가 화면, API, Supabase에서 정상 동작한다. |
| 운동 관리 | `dh`·`dy` | 운동 CRUD가 화면, API, Supabase에서 정상 동작한다. |
| 여행 관리 | `dh`·`dy` | 여행 CRUD가 화면, API, Supabase에서 정상 동작한다. |
| 회원가입 | 공통·통합 담당 | 중복 아이디를 차단하고 비밀번호를 해시하여 `customers` 테이블에 저장한다. |
| 로그인·로그아웃 | 공통·통합 담당 | 올바른 정보로 로그인하고 로그아웃 시 Frontend 로그인 상태가 초기화된다. |
| 회원정보 조회·수정 | 공통·통합 담당 | 로그인한 회원의 공개 정보 조회와 이름·비밀번호 수정이 정상 동작한다. |
| 인증 화면 접근 제어 | 공통·통합 담당 | 로그인 여부에 따라 관리 페이지와 로그인·회원가입 페이지가 구분되어 표시된다. |
| 날짜 관리 | 전체 | 생성 시 두 날짜가 기록되고 수정 시 `updated_at`만 갱신된다. |
| 입력값 검증 | 전체 | 필수값 누락과 잘못된 형식에 422 또는 화면 안내가 표시된다. |
| 예외 처리 | 전체 | 존재하지 않는 ID는 404, DB 실패는 적절한 오류 응답을 반환한다. |
| 프로젝트 통합 | 전체 | 병합 후 FastAPI와 Streamlit이 오류 없이 실행된다. |

각 기능은 Swagger 테스트, Streamlit 화면 테스트, Supabase 반영 확인과 통합 실행을 모두 통과해야 완료로 판단한다.

---

## 3. 팀원별 역할 및 수정 범위

팀원 4명은 각자의 영문 이니셜을 소문자로 사용한 폴더에서 작업한다. Frontend는 `dh`, `dn`, Backend는 `dy`, `tk`가 담당한다.

| 담당자 | 구분 | 담당 기능 | 작업 폴더 | 공통 파일 수정 |
|---|---|---|---|---|
| `dh` | Frontend | 여행·운동 관리 화면 | `frontend/app_pages/dh/` | 없음 |
| `dn` | Frontend | 영화·스터디 관리 화면 | `frontend/app_pages/dn/` | 없음 |
| `dy` | Backend | 여행·운동 API 및 DB 처리 | `backend/app/dy/` | 없음 |
| `tk` | Backend | 영화·스터디 API 및 DB 처리 | `backend/app/tk/` | 없음 |
| 팀장 | 공통·통합 | Router와 Page 등록, 환경설정, 병합 | 공통 파일 | 있음 |

### SQL 및 Supabase 담당

Supabase 프로젝트는 `dn`의 계정에 생성하고 네 명이 함께 사용한다. SQL은 기능별로 한 명씩 담당한다.

| SQL 담당자 | 담당 테이블 | SQL 파일 |
|---|---|---|
| `dy` | 여행 | `backend/sql/dy/travel.sql` |
| `dh` | 운동 | `backend/sql/dh/exercise.sql` |
| `dn` | 스터디 | `backend/sql/dn/study.sql` |
| `tk` | 영화 | `backend/sql/tk/movie.sql` |

### 이니셜 폴더 작업 규칙

- 폴더명은 팀원의 영문 이니셜을 소문자로 작성한다.
- 각 팀원은 자신의 이니셜 폴더 안의 파일만 생성·수정한다.
- Frontend 담당자 2명은 각각 두 개의 관리 화면을 담당한다.
- Backend 담당자 2명은 각각 두 개 테이블의 Router, Schema, Service를 담당한다.
- `backend/app/main.py`, `frontend/app.py`, `core/`, `requirements.txt` 등 공통 파일은 팀장이 관리한다.
- 공통 파일 변경이 필요하면 팀에 공유한 뒤 팀장이 반영하거나 검토한다.
- Frontend와 Backend 담당자는 API 경로, 요청 필드, 응답 형식을 구현 전에 확정한다.

---

## 4. 목표 디렉터리 구조

```text
mini/
└── team01_0803/
    ├── backend/
    │   ├── app/
    │   │   ├── main.py
    │   │   ├── core/
    │   │   │   ├── api_response.py
    │   │   │   ├── supabase_client.py
    │   │   │   └── password.py
    │   │   ├── routers/
    │   │   │   └── auth_router.py
    │   │   ├── schemas/
    │   │   │   └── auth_schema.py
    │   │   ├── services/
    │   │   │   └── auth_service.py
    │   │   ├── dy/                       # 여행·운동 Backend 담당
    │   │   │   ├── routers/
    │   │   │   │   ├── travel_router.py
    │   │   │   │   └── exercise_router.py
    │   │   │   ├── schemas/
    │   │   │   │   ├── travel_schema.py
    │   │   │   │   └── exercise_schema.py
    │   │   │   └── services/
    │   │   │       ├── travel_service.py
    │   │   │       └── exercise_service.py
    │   │   └── tk/                       # 영화·스터디 Backend 담당
    │   │       ├── routers/
    │   │       │   ├── movie_router.py
    │   │       │   └── study_router.py
    │   │       ├── schemas/
    │   │       │   ├── movie_schema.py
    │   │       │   └── study_schema.py
    │   │       └── services/
    │   │           ├── movie_service.py
    │   │           └── study_service.py
    │   ├── sql/
    │   │   ├── customer.sql
    │   │   ├── dy/travel.sql
    │   │   ├── dh/exercise.sql
    │   │   ├── dn/study.sql
    │   │   └── tk/movie.sql
    │   ├── tests/
    │   ├── .env.example
    │   ├── README.md
    │   └── requirements.txt
    ├── frontend/
    │   ├── app.py
    │   ├── app_pages/
    │   │   ├── 00_login.py
    │   │   ├── 00_signup.py
    │   │   ├── mypage.py
    │   │   ├── dn/                       # 영화·스터디 Frontend 담당
    │   │   │   ├── 01_study.py
    │   │   │   └── 02_movie.py
    │   │   └── dh/                       # 여행·운동 Frontend 담당
    │   │       ├── 03_exercise.py
    │   │       └── 04_travel.py
    │   ├── core/
    │   │   ├── api_client.py
    │   │   └── auth.py
    │   ├── clients/
    │   │   └── auth_client.py
    │   ├── .env.example
    │   ├── README.md
    │   └── requirements.txt
    ├── .gitignore
    ├── PLAN.md
    └── README.md
```

| 경로 | 역할 |
|---|---|
| Backend 담당자의 `routers/` | HTTP 요청과 응답을 처리한다. |
| Backend 담당자의 `schemas/` | 요청·응답 자료형과 필수 조건을 검증한다. |
| Backend 담당자의 `services/` | Supabase CRUD를 수행한다. |
| `backend/app/core/` | DB 연결과 공통 응답을 관리한다. |
| 공통 `auth_router.py`, `auth_schema.py`, `auth_service.py` | 회원가입, 로그인, 로그아웃, 회원정보 기능을 관리한다. |
| `backend/app/core/password.py` | 비밀번호 해시 생성과 검증을 담당한다. |
| `backend/sql/` | 테이블 생성 SQL을 관리한다. |
| Frontend 담당자의 이니셜 폴더 | 담당 Streamlit 화면을 관리한다. |
| `frontend/core/` | Backend API 요청 코드를 공통 관리한다. |
| `frontend/clients/auth_client.py` | 인증 관련 Backend API 호출을 관리한다. |

---

## 5. 이름 및 작성 규칙

| 대상 | 규칙 | 예시 |
|---|---|---|
| 이니셜 폴더 | 소문자 영문 | `dy` |
| Python 파일 | 소문자 `snake_case` | `study_service.py` |
| 함수 | 동사와 대상 조합 | `create_study()` |
| 클래스 | `PascalCase` | `StudyCreate` |
| 변수 | `snake_case` | `study_id` |
| 테이블 | 소문자 복수형 | `studies` |
| API 경로 | 리소스 중심 복수형 | `/studies/{study_id}` |
| 환경변수 | 대문자 `SNAKE_CASE` | `SUPABASE_URL` |

- `schema`로 표기하고 `scheme`은 사용하지 않는다.
- Router는 요청·응답, Service는 Supabase 처리를 담당한다.
- Frontend는 Supabase를 직접 호출하지 않고 FastAPI를 호출한다.
- 모든 날짜는 `timestamp`를 사용한다.

---

## 6. API 및 데이터베이스 계획

### 6-1. API 명세

각 리소스는 동일한 CRUD 규칙을 적용한다.

#### 인증 API

| 기능 | 메서드 | 경로 | 요청값 | 성공 | 주요 실패 |
|---|---|---|---|---|---|
| 회원가입 | POST | `/auth/create` | 아이디, 비밀번호, 이름 | 200, 공개 회원정보 | 409, 422, 500 |
| 로그인 | POST | `/auth/signin` | 아이디, 비밀번호 | 200, 공개 회원정보 | 401, 422 |
| 로그아웃 | GET | `/auth/signout/{input_id}` | 회원 ID | 200 | 404 |
| 마이페이지 | GET | `/auth/mypage/{input_id}` | 회원 ID | 200, 공개 회원정보 | 404 |
| 회원정보 수정 | PUT | `/auth/update` | 아이디, 비밀번호, 이름 | 200, 수정 회원정보 | 404, 422, 500 |

인증 응답에는 비밀번호 해시를 포함하지 않고 회원 ID와 이름만 반환한다.

| 기능 | 메서드 | 경로 | 성공 | 주요 실패 |
|---|---|---|---|---|
| 생성 | POST | `/studies`, `/movies`, `/exercises`, `/travels` | 201 | 422, 500 |
| 목록 조회 | GET | 각 리소스 기본 경로 | 200 | 200 빈 목록 |
| 단건 조회 | GET | `/{resource}/{id}` | 200 | 404 |
| 수정 | PUT | `/{resource}/{id}` | 200 | 404, 422 |
| 삭제 | DELETE | `/{resource}/{id}` | 204 | 404 |

### 6-2. 데이터베이스 명세

#### 테이블: `customers`

| 컬럼 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `id` | `text` | Y | 로그인에 사용하는 회원 ID, 기본키 |
| `pwd` | `text` | Y | 평문이 아닌 해시 처리된 비밀번호 |
| `name` | `text` | Y | 회원 이름 |

비밀번호는 Backend에서 해시한 후 저장하며 Frontend와 API 응답에 노출하지 않는다. 이번 범위에서는 참고 프로젝트와 동일하게 Frontend 세션 상태로 로그인 화면 접근을 제어한다.

#### 테이블: `studies`

| 컬럼 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `id` | `bigint` | Y | 자동 증가 ID |
| `title` | `text` | Y | 스터디 제목 |
| `subject` | `text` | Y | 학습 주제 |
| `study_date` | `date` | Y | 예정일 |
| `location` | `text` | N | 장소 또는 온라인 주소 |
| `description` | `text` | N | 상세 내용 |
| `created_at` | `timestamp` | Y | 입력일시 |
| `updated_at` | `timestamp` | Y | 수정일시 |

#### 테이블: `movies`

| 컬럼 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `id` | `bigint` | Y | 자동 증가 ID |
| `title` | `text` | Y | 영화 제목 |
| `genre` | `text` | N | 장르 |
| `director` | `text` | N | 감독 |
| `release_date` | `date` | N | 개봉일 |
| `rating` | `numeric(3,1)` | N | 평점 0~10 |
| `review` | `text` | N | 감상평 |
| `created_at` | `timestamp` | Y | 입력일시 |
| `updated_at` | `timestamp` | Y | 수정일시 |

#### 테이블: `exercises`

| 컬럼 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `id` | `bigint` | Y | 자동 증가 ID |
| `exercise_name` | `text` | Y | 운동명 |
| `exercise_date` | `date` | Y | 운동일 |
| `duration_minutes` | `integer` | Y | 운동 시간(분) |
| `intensity` | `text` | N | 운동 강도 |
| `calories` | `integer` | N | 예상 소모 칼로리 |
| `memo` | `text` | N | 메모 |
| `created_at` | `timestamp` | Y | 입력일시 |
| `updated_at` | `timestamp` | Y | 수정일시 |

#### 테이블: `travels`

| 컬럼 | 타입 | 필수 | 설명 |
|---|---|---|---|
| `id` | `bigint` | Y | 자동 증가 ID |
| `destination` | `text` | Y | 여행지 |
| `start_date` | `date` | Y | 출발일 |
| `end_date` | `date` | Y | 종료일 |
| `budget` | `integer` | N | 예상 비용 |
| `transportation` | `text` | N | 이동 수단 |
| `memo` | `text` | N | 메모 |
| `created_at` | `timestamp` | Y | 입력일시 |
| `updated_at` | `timestamp` | Y | 수정일시 |

공통 날짜 컬럼은 다음 기준을 사용한다.

```sql
created_at timestamp not null default now(),
updated_at timestamp not null default now()
```

수정 시 `updated_at`을 자동 갱신하는 공통 Trigger를 네 테이블에 적용한다. 평점은 0~10, 운동 시간은 1분 이상, 칼로리와 예산은 0 이상이며 여행 종료일은 시작일보다 빠를 수 없다.

---

## 7. 개발 일정

| 단계 | 작업 | 담당자 | 결과물 |
|---|---|---|---|
| 1 | 요구사항, 컬럼, 실제 이니셜 확정 | 전체 | 확정 계획서 |
| 2 | GitHub와 공통 폴더 생성 | 팀장 | 초기 저장소 |
| 3 | `dn`의 Supabase 프로젝트와 환경변수 준비 | `dn` | 공유 개발 환경 |
| 4 | 테이블별 SQL 작성 및 검토 | `dy`·`dh`·`dn`·`tk` | SQL 4개 |
| 5 | 검토된 SQL을 Supabase에 적용 | `dn`·각 SQL 담당자 | 테이블 4개 |
| 6 | 이니셜 폴더에서 Backend 구현 | Backend 2명 | API 코드 |
| 7 | Swagger 개별 테스트 | Backend 2명 | 테스트 결과 |
| 8 | 이니셜 폴더에서 Frontend 구현 | Frontend 2명 | 화면 코드 |
| 9 | 기능별 Pull Request | 각 담당자 | PR 4개 |
| 10 | 공통 파일 등록과 `develop` 병합 | 팀장 | 통합 코드 |
| 11 | 전체 기능과 충돌 테스트 | 전체 | 실행 프로젝트 |
| 12 | README와 발표 자료 정리 | 전체 | 최종 문서 |

---

## 8. 실행 및 테스트 방법

### 8-1. Backend 실행

```powershell
cd mini\team01_0803\backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger: `http://127.0.0.1:8000/docs`

### 8-2. Frontend 실행

```powershell
cd mini\team01_0803\frontend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
streamlit run app.py
```

Streamlit: `http://localhost:8501`

### 8-3. 환경변수

Backend `.env.example`:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
```

Frontend `.env.example`:

```env
BACKEND_API_URL=http://127.0.0.1:8000
```

---

## 9. 테스트 체크리스트

- [ ] Backend와 Frontend가 오류 없이 실행된다.
- [ ] Swagger와 Streamlit에 네 기능이 표시된다.
- [ ] 회원가입 시 `customers` 테이블에 비밀번호 해시가 저장된다.
- [ ] 중복 아이디 회원가입이 409로 처리된다.
- [ ] 올바른 아이디와 비밀번호로 로그인할 수 있다.
- [ ] 틀린 로그인 정보가 401로 처리된다.
- [ ] 로그아웃 후 로그인 상태와 브라우저 세션 정보가 삭제된다.
- [ ] 마이페이지에서 회원정보를 조회하고 수정할 수 있다.
- [ ] 인증 API 응답과 화면에 비밀번호 또는 해시값이 노출되지 않는다.
- [ ] 로그인 여부에 따라 접근 가능한 Streamlit 페이지가 구분된다.
- [ ] 네 테이블에서 생성·조회·수정·삭제가 정상 동작한다.
- [ ] 빈 목록이 오류 없이 표시된다.
- [ ] 존재하지 않는 ID가 404로 처리된다.
- [ ] 필수값 누락과 잘못된 값이 검증된다.
- [ ] 생성 시 입력일시와 수정일시가 기록된다.
- [ ] 수정 시 수정일시만 변경된다.
- [ ] Frontend 화면에서 Backend API 결과를 확인할 수 있다.
- [ ] 네 명의 브랜치를 병합한 뒤 전체 프로젝트가 실행된다.
- [ ] 실제 Supabase 키가 Git에 포함되지 않는다.

자동화 테스트를 작성할 경우 정상 응답, 422, 404, Supabase 실패 Mock을 `pytest`로 검증한다.

---

## 10. Git 협업 및 공통 파일 관리

### 10-1. 브랜치 구성

```text
main
└── develop
    ├── feature/dn-frontend
    ├── feature/dh-frontend
    ├── feature/dy-backend
    └── feature/tk-backend
```

실제 브랜치 이름에는 각 팀원의 실제 이니셜을 사용한다. `main`은 최종 버전, `develop`은 통합 테스트, `feature/{이니셜}-{역할}`은 개인 작업 브랜치로 사용한다.

### 10-2. 커밋 메시지

| 구분 | 의미 | 예시 |
|---|---|---|
| `feat` | 기능 추가 | `feat: 영화 CRUD API 추가` |
| `fix` | 오류 수정 | `fix: 여행 날짜 검증 수정` |
| `docs` | 문서 수정 | `docs: Supabase 설정 추가` |
| `refactor` | 구조 개선 | `refactor: 운동 DB 로직 분리` |
| `test` | 테스트 추가 | `test: 스터디 조회 테스트 추가` |
| `chore` | 설정 변경 | `chore: backend 의존성 추가` |

### 10-3. 공통 파일 관리

| 공통 파일 | 담당자 | 확인 방법 |
|---|---|---|
| `backend/app/main.py` | 팀장 | Swagger에서 Router 확인 |
| `frontend/app.py` | 팀장 | 전체 메뉴 확인 |
| `supabase_client.py` | 팀장 | 네 Service 실행 확인 |
| `api_client.py` | 팀장 | 네 화면 실행 확인 |
| 인증 Router, Schema, Service | 팀장 또는 공통·통합 담당 | 회원가입·로그인·로그아웃·마이페이지 확인 |
| `password.py`, `auth.py`, `auth_client.py` | 팀장 또는 공통·통합 담당 | 비밀번호 해시와 로그인 상태 확인 |
| `requirements.txt` | 팀장 | 새 환경에서 설치 확인 |
| `.env.example`, `.gitignore` | 팀장 | 비밀값과 Git 추적 확인 |

공통 파일은 임의로 수정하지 않는다. 변경이 필요하면 먼저 공유하고 팀장이 반영하거나 검토한다.

---

## 11. Supabase 공동 개발, 환경변수 및 보안

### 11-1. 하나의 Supabase 프로젝트로 네 명이 개발하는 방법

1. `dn`이 자신의 Supabase 계정에 프로젝트 하나를 생성한다.
2. 가능하면 로그인 계정을 공유하지 않고 각 팀원을 프로젝트 멤버로 초대한다.
3. 초대 기능을 사용하기 어렵다면 팀장이 DB 구조 변경을 전담한다.
4. 네 팀원은 동일한 URL과 개발용 키를 각자의 로컬 `.env`에 설정한다.
5. Frontend는 Supabase에 직접 연결하지 않고 Backend API만 호출한다.
6. `dy`는 여행, `dh`는 운동, `dn`은 스터디, `tk`는 영화 SQL을 각자의 폴더에 작성한다.
7. Pull Request로 SQL을 검토한 후 `dn`과 각 SQL 담당자가 Supabase SQL Editor에서 적용한다.
8. 적용된 SQL은 GitHub에 남겨 모든 팀원이 같은 DB 구조를 확인한다.

### 11-2. 충돌 방지 규칙

- 담당 테이블이 아닌 다른 테이블을 직접 변경하지 않는다.
- Dashboard에서 즉흥적으로 컬럼을 수정하지 않는다.
- 컬럼 변경은 SQL 파일과 계획서에 먼저 반영한다.
- 테이블 또는 컬럼 삭제는 전체 동의 후 진행한다.
- 공통 Trigger는 팀장이 관리한다.
- 공통 파일과 SQL 변경은 별도 커밋으로 분리한다.

### 11-3. 보안 체크

- [ ] `.env`와 실제 Supabase 키를 GitHub에 올리지 않는다.
- [ ] API 키를 코드에 직접 작성하지 않는다.
- [ ] Frontend에서 service-role/secret 키를 사용하지 않는다.
- [ ] 회원 비밀번호는 평문으로 저장하지 않고 안전한 해시 함수로 저장한다.
- [ ] 인증 API 응답, 로그, 오류 메시지에 비밀번호와 해시값을 출력하지 않는다.
- [ ] Frontend 세션에는 비밀번호를 저장하지 않는다.
- [ ] 로그아웃 시 Frontend 세션과 브라우저 저장소의 로그인 정보를 삭제한다.
- [ ] 로그와 오류 메시지에 비밀키를 출력하지 않는다.
- [ ] `.env.example`에는 변수 이름과 예시값만 기록한다.
- [ ] RLS 사용 여부와 정책을 팀에서 통일한다.
- [ ] 프로젝트 종료 후 공유한 키를 교체한다.
- [ ] 키가 GitHub에 노출되면 즉시 재발급한다.

권장 `.gitignore`:

```gitignore
.env
.env.*
!.env.example
.venv/
__pycache__/
*.pyc
.pytest_cache/
.streamlit/secrets.toml
```
