import pandas as pd
from sqlalchemy import create_engine, text
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
                pool_recycle=3600,  # Recycle connections every hour
            )
            # print(f"Database Engine initialized for {database} at {host} ({self._key})")

    @property
    def engine(self):
        if self._engine is None:
            raise RuntimeError(
                f"DatabaseManager '{self}' not initialized. Call initialize() first."
            )
        return self._engine

    def get_df(self, sql: str, params: Optional[dict[str, Any]] = None) -> pd.DataFrame:
        """Executes a SELECT query and returns a Pandas DataFrame."""
        return pd.read_sql(text(sql), con=self.engine, params=params)

    def execute(self, sql: str, params: Optional[dict[str, Any]] = None) -> Any:
        """Executes an INSERT, UPDATE, or DELETE query."""
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params)
            conn.commit()
            return result

    def insert_df(self, df: pd.DataFrame, table_name: str, if_exists: str = "append"):
        """Inserts a DataFrame into a database table."""
        df.to_sql(table_name, con=self.engine, if_exists=if_exists, index=False)

    def insert_dict(self, table_name: str, data: dict[str, Any]):
        """Inserts a dictionary of data into a database table."""
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f":{k}" for k in data.keys()])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return self.execute(sql, data)
