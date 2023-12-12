from typing import Union

from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.pool.impl import SingletonThreadPool

from .errors import ConfigurationError
from .settings import AllDatabaseSettings


def get_engine(
    stg: AllDatabaseSettings, is_async: bool = False
) -> Union[Engine, AsyncEngine]:
    """
    Creates an engine based on settings.

    Args:
        stg: The database settings.
        is_async: Whether to create an async engine.
    Raises:
        ConfigurationError: If the database URL is not set.
    """
    if not stg.db.url:
        raise ConfigurationError("A database connection string is required")

    # Common arguments.
    engine_args = {
        **stg.db.model_dump(),
    }

    # Dialect-specific arguments.
    if stg.db.url.startswith("sqlite"):
        engine_args.update(stg.sqlite_db.model_dump())
        engine_args["poolclass"] = SingletonThreadPool
    elif stg.db.url.startswith("postgres"):
        engine_args.update(stg.pg_db.model_dump())

    # Create the engine.
    engine: Union[Engine, AsyncEngine]
    if is_async:
        from sqlalchemy.ext.asyncio import create_async_engine

        if "pool_size" in engine_args:
            del engine_args["pool_size"]
        if "sync_alternative" in engine_args:
            del engine_args["sync_alternative"]
        engine = create_async_engine(**engine_args)
    else:
        if stg.db.sync_alternative:
            engine_args["url"] = stg.db.sync_alternative
        if "sync_alternative" in engine_args:
            del engine_args["sync_alternative"]
        engine = create_engine(**engine_args)
    return engine
