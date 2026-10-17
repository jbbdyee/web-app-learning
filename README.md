# Web App Learning

이전 교육 과정에서 Streamlit 화면과 FastAPI 백엔드를 연결하며 웹앱의 기본 흐름을 익힌 실습 저장소입니다.

## 이 과정에서 배운 것

- **화면과 API 연결:** Streamlit 멀티페이지 화면에서 FastAPI API를 호출하고 응답을 표시했습니다.
- **인증과 데이터:** 로그인·JWT·비밀번호 처리부터 Supabase 데이터 저장과 RLS 권한 검사까지 단계별로 실습했습니다.
- **사용자 기능:** 상품 조회·관리, 파일 업로드와 실시간 데이터 표시를 화면과 백엔드에 연결했습니다.

## 주요 실습

| 주제 | 폴더 |
| --- | --- |
| Streamlit 화면 구성과 API 연동 | [`mini_frontend/`](mini_frontend/), [`mini_frontend_02/`](mini_frontend_02/) |
| 로그인·JWT·DB·RLS 단계별 확장 | [`mini_frontend_login/`](mini_frontend_login/), [`login_jwt/`](login_jwt/), [`login_jwt_db/`](login_jwt_db/), [`login_jwt_db_rls_product/`](login_jwt_db_rls_product/) |
| 업로드와 실시간 데이터 | [`mini_frontend_upload/`](mini_frontend_upload/), [`realtime_data_simple/`](realtime_data_simple/) |

실행 방법은 해당 폴더 또는 하위 `frontend`·`backend`의 안내 문서를 확인해 주세요. 이 저장소는 여러 단계의 수업 예제를 모은 기록이며, 하나의 완성된 서비스는 아닙니다.
