from sqlalchemy import Engine, text
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.pool.impl import SingletonThreadPool

from db4me.connection import get_engine
from db4me.settings import AllDatabaseSettings


def test_get_engine_sync():
    """
    Test get_engine with a sync engine.
    """
    stg = AllDatabaseSettings()
    stg.db.url = "sqlite://"
    engine = get_engine(stg)
    assert isinstance(engine, Engine)
    assert isinstance(engine.pool, SingletonThreadPool)
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY);"))
        conn.execute(text("INSERT INTO test VALUES (1);"))


async def test_get_engine_async():
    """
    Test get_engine with an async engine.
    """
    stg = AllDatabaseSettings()
    stg.db.url = "sqlite+aiosqlite://"
    engine = get_engine(stg, is_async=True)
    assert isinstance(engine, AsyncEngine)
    assert isinstance(engine.pool, SingletonThreadPool)
    async with engine.connect() as conn:
        await conn.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY);"))
        await conn.execute(text("INSERT INTO test VALUES (1);"))
