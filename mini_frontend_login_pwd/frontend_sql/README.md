# frontend_sql

`backend_sql`을 호출하는 Streamlit 프론트엔드입니다. 기존 화면과 로그인 세션 동작은 유지합니다.

## 환경변수

기본 백엔드 주소는 `http://127.0.0.1:8001`입니다. 변경이 필요하면 `.env.example`을 참고해 `.env`를 만듭니다.

```env
BACKEND_API_URL=http://127.0.0.1:8001
```

## 설치 및 실행

먼저 `backend_sql`을 8001 포트에서 실행한 뒤 다음 명령을 사용합니다.

```powershell
cd frontend_sql
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.port 8502
```

Streamlit: `http://localhost:8502`
