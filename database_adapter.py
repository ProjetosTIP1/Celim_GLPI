import time
import pandas as pd
from sqlalchemy import create_engine, text, exc
from urllib.parse import quote_plus
from typing import Any, Optional


class DatabaseManager:
    """
    Synchronous Database Manager using SQLAlchemy for connection pooling and
    clean integration with Pandas.
    """

    _instances: dict[str, "DatabaseManager"] = {}

    def __new__(cls, key: str = "default"):
        if key not in cls._instances:
            instance = super(DatabaseManager, cls).__new__(cls)
            instance._engine = None
            instance._key = key
            cls._instances[key] = instance
        return cls._instances[key]

    def initialize(
        self,
        user: str,
        password: str,
        host: str,
        database: str,
        port: int = 3306,
        driver: str = "mysql+pymysql",
    ) -> None:
        """Initializes the database engine if not already initialized."""
        if self._engine is None:
            safe_password = quote_plus(password)
            connection_string = (
                f"{driver}://{user}:{safe_password}@{host}:{port}/{database}"
            )
            self._engine = create_engine(
                connection_string,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,  # Validates connections before use
                pool_recycle=120,  # Recycle connections every 2 minutes (lower to avoid stale connections)
                pool_timeout=30,  # Timeout for getting a connection from the pool
            )
            # print(f"Database Engine initialized for {database} at {host} ({self._key})")

    @property
    def engine(self):
        if self._engine is None:
            raise RuntimeError(
                f"DatabaseManager '{self}' not initialized. Call initialize() first."
            )
        return self._engine

    def get_df(
        self,
        sql: str,
        params: Optional[dict[str, Any]] = None,
        retries: int = 3,
        delay: int = 2,
    ) -> pd.DataFrame:
        """Executes a SELECT query and returns a Pandas DataFrame with retry logic."""
        for attempt in range(retries):
            try:
                return pd.read_sql(text(sql), con=self.engine, params=params)
            except (exc.OperationalError, exc.DBAPIError) as e:
                if attempt < retries - 1:
                    print(
                        f"Database connection error on {self._key}: {e}. Retrying {attempt + 1}/{retries} in {delay}s..."
                    )
                    time.sleep(delay)
                else:
                    print(
                        f"Database connection failed on {self._key} after {retries} attempts."
                    )
                    raise

    def execute(
        self,
        sql: str,
        params: Optional[dict[str, Any]] = None,
        retries: int = 3,
        delay: int = 2,
    ) -> Any:
        """Executes an INSERT, UPDATE, or DELETE query with retry logic."""
        for attempt in range(retries):
            try:
                with self.engine.connect() as conn:
                    result = conn.execute(text(sql), params)
                    conn.commit()
                    return result
            except (exc.OperationalError, exc.DBAPIError) as e:
                if attempt < retries - 1:
                    print(
                        f"Database execution error on {self._key}: {e}. Retrying {attempt + 1}/{retries} in {delay}s..."
                    )
                    time.sleep(delay)
                else:
                    print(
                        f"Database execution failed on {self._key} after {retries} attempts."
                    )
                    raise

    def insert_df(self, df: pd.DataFrame, table_name: str, if_exists: str = "append"):
        """Inserts a DataFrame into a database table."""
        df.to_sql(table_name, con=self.engine, if_exists=if_exists, index=False)

    def insert_dict(self, table_name: str, data: dict[str, Any]):
        """Inserts a dictionary of data into a database table."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f":{k}" for k in data.keys()])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return self.execute(sql, data)

    def dispose(self):
        """Disposes the engine and closes all connections in the pool."""
        if self._engine:
            self._engine.dispose()
            self._engine = None
            # print(f"Database Engine for {self._key} disposed.")

    @classmethod
    def dispose_all(cls):
        """Disposes all registered DatabaseManager instances."""
        for key, instance in cls._instances.items():
            instance.dispose()
        cls._instances.clear()
