-- Supabase Dashboard > SQL Editor에서 실행합니다.
-- shop.products의 id는 BIGINT 자동 증가 값입니다.

CREATE SCHEMA IF NOT EXISTS shop;

CREATE TABLE IF NOT EXISTS shop.users (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL DEFAULT '',
    role TEXT NOT NULL DEFAULT 'user' CHECK (role IN ('user', 'admin'))
);

-- 신규 Supabase Auth 사용자를 shop.users에도 자동 등록합니다.
CREATE OR REPLACE FUNCTION shop.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = ''
AS $$
BEGIN
    INSERT INTO shop.users (user_id, name)
    VALUES (NEW.id, COALESCE(NEW.raw_user_meta_data ->> 'name', ''))
    ON CONFLICT (user_id) DO NOTHING;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
AFTER INSERT ON auth.users
FOR EACH ROW EXECUTE FUNCTION shop.handle_new_user();

-- 트리거 생성 전에 가입한 기존 사용자도 빠짐없이 등록합니다.
INSERT INTO shop.users (user_id, name)
SELECT id, COALESCE(raw_user_meta_data ->> 'name', '')
FROM auth.users
ON CONFLICT (user_id) DO NOTHING;

CREATE SEQUENCE IF NOT EXISTS shop.products_id_seq;

CREATE TABLE IF NOT EXISTS shop.products (
    id BIGINT DEFAULT nextval('shop.products_id_seq') PRIMARY KEY,
    name TEXT NOT NULL CHECK (char_length(name) BETWEEN 1 AND 100),
    price INTEGER NOT NULL CHECK (price >= 0)
);

-- 기존 테이블에도 자동 증가 기본값을 적용합니다.
ALTER TABLE shop.products
    ALTER COLUMN id TYPE BIGINT USING id::bigint;
ALTER SEQUENCE shop.products_id_seq OWNED BY shop.products.id;
ALTER TABLE shop.products
    ALTER COLUMN id SET DEFAULT nextval('shop.products_id_seq');
ALTER TABLE shop.products
    ALTER COLUMN id SET NOT NULL;

-- 기존 데이터의 가장 큰 ID 다음 번호부터 발급합니다.
SELECT setval(
    'shop.products_id_seq',
    COALESCE((SELECT MAX(id) FROM shop.products), 0) + 1,
    false
);

ALTER TABLE shop.products ENABLE ROW LEVEL SECURITY;
ALTER TABLE shop.users ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "자신의 사용자 정보 조회" ON shop.users;
CREATE POLICY "자신의 사용자 정보 조회"
ON shop.users FOR SELECT TO authenticated
USING ((SELECT auth.uid()) = user_id);

DROP POLICY IF EXISTS "로그인 사용자의 상품 조회" ON shop.products;
DROP POLICY IF EXISTS "로그인 사용자의 상품 생성" ON shop.products;
DROP POLICY IF EXISTS "로그인 사용자의 상품 수정" ON shop.products;
DROP POLICY IF EXISTS "로그인 사용자의 상품 삭제" ON shop.products;
DROP POLICY IF EXISTS "관리자의 상품 생성" ON shop.products;
DROP POLICY IF EXISTS "관리자의 상품 수정" ON shop.products;
DROP POLICY IF EXISTS "관리자의 상품 삭제" ON shop.products;

CREATE POLICY "로그인 사용자의 상품 조회"
ON shop.products FOR SELECT TO authenticated
USING (true);

CREATE POLICY "관리자의 상품 생성"
ON shop.products FOR INSERT TO authenticated
WITH CHECK (
    EXISTS (
        SELECT 1 FROM shop.users
        WHERE user_id = (SELECT auth.uid()) AND role = 'admin'
    )
);

CREATE POLICY "관리자의 상품 수정"
ON shop.products FOR UPDATE TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM shop.users
        WHERE user_id = (SELECT auth.uid()) AND role = 'admin'
    )
)
WITH CHECK (
    EXISTS (
        SELECT 1 FROM shop.users
        WHERE user_id = (SELECT auth.uid()) AND role = 'admin'
    )
);

CREATE POLICY "관리자의 상품 삭제"
ON shop.products FOR DELETE TO authenticated
USING (
    EXISTS (
        SELECT 1 FROM shop.users
        WHERE user_id = (SELECT auth.uid()) AND role = 'admin'
    )
);

GRANT USAGE ON SCHEMA shop TO authenticated;
GRANT SELECT ON shop.users TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON shop.products TO authenticated;
GRANT USAGE, SELECT ON SEQUENCE shop.products_id_seq TO authenticated;

-- 관리자 권한 부여 예시 (아래 주석을 해제하고 이메일을 변경한 뒤 실행):
-- UPDATE shop.users AS u
-- SET role = 'admin'
-- FROM auth.users AS au
-- WHERE u.user_id = au.id
--   AND au.email = 'admin@example.com';

-- 사용자 UUID를 알고 있는 경우:
-- UPDATE shop.users
-- SET role = 'admin'
-- WHERE user_id = '00000000-0000-0000-0000-000000000000';

-- 일반 사용자로 되돌리는 경우에는 SET role = 'user'로 변경합니다.
