-- Docker의 agent_db 데이터베이스에 접속한 뒤 실행합니다.

CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    pwd TEXT NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    price INTEGER NOT NULL CHECK (price >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS carts (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES customers(id),
    item_id TEXT NOT NULL REFERENCES products(id),
    count INTEGER NOT NULL CHECK (count >= 1),
    created_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_carts_user_id ON carts(user_id);
CREATE INDEX IF NOT EXISTS idx_carts_item_id ON carts(item_id);
