"""Pydantic models used in configuring the database."""
from typing import Any, Callable, Optional, cast

from pydantic import BaseModel, Field, ValidationInfo, field_validator


class SqliteDatabaseSettings(BaseModel):
    """
    Settings for connections to SqLite databases.
    """

    connect_args: Optional[dict] = Field(
        default_factory=dict,
        description="Arguments for the sqlite3.connect() function.",
    )


class PgDatabaseSettings(BaseModel):
    """
    Settings for connections to postgres databases.
    """

    pass


class DatabaseSettings(BaseModel):
    """
    Common settings for all database types.

    Attributes:
        url: The database URL. In case of async connections this is where the
            async database URL should be set.
        sync_alternative: The database URL to use for sync connections. This
            should be used when an async connection exists in `url`. If missing
            an attempt will be made to convert the async URL to a sync URL.
        echo: If True, the engine will log all statements as well as a
            repr() of their parameter lists to the engines logger, which
            defaults to sys.stdout.
        pool_size: The size of the database pool.
        pool_recycle: The number of seconds after which a database connection
            should be recycled.
        pool_pre_ping: If True, the database connection pool will be pre-pinged
            This means that the connection will be checked if it is still
            alive before it is used.
        pool_reset_on_return: The action to take when a connection is returned
            to the pool. Possible values are:
                - "rollback": Rollback the transaction.
                - "commit": Commit the transaction.
                - "disconnect": Disconnect the connection.
    """

    # Database URL
    url: Optional[str] = "sqlite://"

    # Database alternative URL.
    sync_alternative: Optional[str] = Field(None, validate_default=True)

    # Database echo
    echo: Optional[bool] = False

    # Database pool size
    pool_size: Optional[int] = 10

    # Database pool recycle
    pool_recycle: Optional[int] = 3600

    # Database pool pre ping
    pool_pre_ping: Optional[bool] = True

    # Database pool reset on return
    pool_reset_on_return: Optional[str] = "rollback"

    @field_validator("sync_alternative")
    @classmethod
    def validate_sync_alternative(cls, v, values: ValidationInfo):
        """
        Validate the sync_alternative field.
        """
        url = values.data.get("url")
        if v is None and url is not None:
            if url.startswith("postgresql+asyncpg"):
                v = url.replace("postgresql+asyncpg", "postgresql")
            elif url.startswith("sqlite+aiosqlite"):
                v = url.replace("sqlite+aiosqlite", "sqlite")
        return v


class AllDatabaseSettings(BaseModel):
    """
    Settings for the database connection.
    """

    db: DatabaseSettings = Field(
        default_factory=cast(Callable[[], Any], DatabaseSettings),
        description="Database settings.",
    )
    pg_db: PgDatabaseSettings = Field(
        default_factory=PgDatabaseSettings,
        description="Database settings specific for postgres.",
    )
    sqlite_db: SqliteDatabaseSettings = Field(
        default_factory=SqliteDatabaseSettings,
        description="Database settings specific for SqLite.",
    )
