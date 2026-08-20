"""로컬 PostgreSQL 연결과 SQLAlchemy 세션을 관리합니다."""

from __future__ import annotations

import os
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Iterator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


class Base(DeclarativeBase):
    pass


def get_database_url() -> str:
    database_url = os.getenv("DATABASE_URL", "").strip()
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL이 없습니다. backend_sql/.env 파일을 확인하세요."
        )
    if "your_password" in database_url:
        raise RuntimeError(
            "DATABASE_URL에 예시 비밀번호가 남아 있습니다. 실제 접속 정보를 입력하세요."
        )
    # 일반적인 postgresql:// URL도 이 프로젝트의 Psycopg 3 드라이버로 연결합니다.
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )
    return database_url


@lru_cache
def get_engine() -> Engine:
    return create_engine(get_database_url(), pool_pre_ping=True)


def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), expire_on_commit=False)


@contextmanager
def session_scope() -> Iterator[Session]:
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
