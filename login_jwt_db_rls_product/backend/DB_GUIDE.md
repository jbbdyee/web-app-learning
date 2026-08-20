# Supabase 설정

Supabase Auth는 회원을 관리하고, 상품 데이터는 `shop.products` 테이블에 저장합니다.

## 1. 테이블과 정책 만들기

Supabase Dashboard의 **SQL Editor**에서 [schema.sql](schema.sql) 전체를 실행합니다. 이 스크립트는 다음 항목을 구성합니다.

- `shop.users`: Supabase Auth 사용자와 `user`/`admin` 역할
- `shop.products`: 상품 데이터
- 신규 가입자를 일반 사용자로 등록하는 트리거
- 로그인 사용자의 상품 조회 정책
- 관리자만 허용하는 상품 생성·수정·삭제 정책

기본 가입 역할은 `user`입니다. 관리자로 지정할 계정은 `schema.sql` 마지막의 관리자 권한 부여 예시를 사용해 `role = 'admin'`으로 변경합니다.

## 2. RLS 권한

- `authenticated` 사용자는 상품을 조회할 수 있습니다.
- `shop.users.role = 'admin'`인 사용자만 상품을 생성·수정·삭제할 수 있습니다.
- 공개 키와 사용자 Access Token을 사용하므로 직접 REST 요청을 보내도 RLS가 적용됩니다.

## 3. 환경 변수

`backend/.env`에 다음 두 값만 넣습니다.

```env
SUPABASE_URL=https://프로젝트-ID.supabase.co
SUPABASE_PUBLISHABLE_KEY=publishable-key-또는-anon-key
```

기존 프로젝트에서 `SUPABASE_ANON_KEY`라는 이름을 사용 중이라면 그대로 두어도 됩니다.

백엔드는 로그인 시 받은 Access Token을 Supabase Data API에 그대로 전달합니다. 따라서 `service_role` 키가 필요 없고 RLS도 우회하지 않습니다.
