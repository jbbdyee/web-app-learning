# 통합 개발 환경 설정

이 문서는 Streamlit 프런트엔드와 FastAPI 백엔드를 로컬에서 함께 실행하는 방법을 설명한다. 아래 명령은 프로젝트 루트 `mini_frontend_02_mock`에서 Windows PowerShell로 실행하는 것을 기준으로 한다.

## 1. 사전 준비

| 항목 | 권장 사항 |
|---|---|
| Python | 3.11 이상 |
| 터미널 | Windows PowerShell |
| Gemini API 키 | 채팅 API를 실제로 사용할 때 필요 |

Python 설치 여부를 확인한다.

```powershell
python --version
```

프런트엔드와 백엔드는 패키지 버전 충돌을 방지하기 위해 각각 별도의 가상환경을 사용한다.

## 2. 백엔드 설정

프로젝트 루트에서 다음 명령을 실행한다.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 백엔드 환경 변수

`backend` 디렉터리에 `.env` 파일을 만들고 다음 값을 입력한다.

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
```

- `GEMINI_API_KEY`에는 발급받은 실제 키를 입력한다.
- `.env` 파일은 비밀값을 포함하므로 Git에 커밋하지 않는다.
- 상품 API와 테스트만 확인할 경우 Gemini API 키 없이도 실행할 수 있지만, 채팅 API 호출은 실패할 수 있다.

### 백엔드 실행

```powershell
python -m uvicorn app.main:app --reload
```

정상 실행 후 다음 주소를 확인한다.

| 용도 | 주소 |
|---|---|
| API 서버 | `http://127.0.0.1:8000` |
| Swagger API 문서 | `http://127.0.0.1:8000/docs` |
| OpenAPI 문서 | `http://127.0.0.1:8000/openapi.json` |

백엔드 서버를 종료하려면 실행 중인 터미널에서 `Ctrl+C`를 누른다.

## 3. 프런트엔드 설정

백엔드를 실행한 터미널은 그대로 두고 새 PowerShell 터미널을 연다. 프로젝트 루트에서 다음 명령을 실행한다.

```powershell
cd frontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 프런트엔드 실행

```powershell
python -m streamlit run app.py
```

Streamlit은 일반적으로 다음 주소에서 실행된다.

```text
http://localhost:8501
```

프런트엔드 서버를 종료하려면 실행 중인 터미널에서 `Ctrl+C`를 누른다.

## 4. 전체 실행 순서

| 순서 | 터미널 | 작업 |
|---|---|---|
| 1 | 터미널 1 | `backend` 가상환경 활성화 |
| 2 | 터미널 1 | FastAPI 서버 실행 |
| 3 | 터미널 2 | `frontend` 가상환경 활성화 |
| 4 | 터미널 2 | Streamlit 서버 실행 |
| 5 | 브라우저 | `http://localhost:8501` 접속 |

백엔드를 먼저 실행해야 프런트엔드의 서버 상태 확인 및 백엔드 연동 기능을 사용할 수 있다.

## 5. 테스트 실행

### 백엔드 테스트

백엔드 가상환경이 활성화된 터미널에서 실행한다.

```powershell
cd backend
python -m pytest
```

이미 `backend` 디렉터리에 있다면 `cd backend`는 생략한다.

현재 프런트엔드에는 별도의 자동화 테스트가 없으므로 Streamlit 실행 후 각 화면을 직접 확인한다.

## 6. 가상환경 다시 활성화하기

터미널을 새로 열었거나 가상환경이 비활성화된 경우 해당 프로젝트 디렉터리에서 다시 활성화한다.

백엔드:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
```

프런트엔드:

```powershell
cd frontend
.\.venv\Scripts\Activate.ps1
```

가상환경을 종료하려면 다음 명령을 사용한다.

```powershell
deactivate
```

## 7. 자주 발생하는 문제

| 문제 | 확인 및 해결 방법 |
|---|---|
| 가상환경 활성화가 차단됨 | PowerShell 실행 정책을 확인하고 현재 사용자 범위에서 스크립트 실행을 허용한다. |
| `ModuleNotFoundError` 발생 | 올바른 프로젝트의 가상환경이 활성화되었는지 확인한 뒤 requirements를 다시 설치한다. |
| 포트 8000을 사용할 수 없음 | 기존 FastAPI 프로세스를 종료하거나 다른 포트로 실행하고 프런트엔드의 백엔드 주소도 함께 변경한다. |
| 프런트엔드에서 백엔드 연결 실패 | FastAPI가 `127.0.0.1:8000`에서 실행 중인지 확인한다. |
| Gemini 채팅 호출 실패 | `backend/.env`의 API 키와 모델명을 확인하고 백엔드를 재시작한다. |
| 날씨 조회 실패 | 인터넷 연결 및 Open-Meteo API 응답 상태를 확인한다. |

## 8. 현재 구현 참고사항

- 프런트엔드의 기본 로그인 정보는 현재 `id01` / `pwd01`로 하드코딩되어 있다.
- 회원가입 정보는 아직 데이터베이스에 저장되지 않는다.
- 상품 API는 현재 예시 데이터를 반환하며 실제 데이터베이스와 연결되어 있지 않다.
- 프런트엔드 서버 확인 화면은 `GET /health`를 호출하지만 현재 백엔드에는 해당 API가 구현되어 있지 않다.
- 위 항목은 [개발 계획서](plan.md)의 단계에 따라 구현할 예정이다.
