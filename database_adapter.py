import urllib.parse
import pandas as pd
from typing import Optional, Any
from sqlalchemy import create_engine, text
from settings import settings


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
        if self._engine is None:
            safe_password = urllib.parse.quote_plus(password)
            connection_string = f"{driver}://{user}:{safe_password}@{host}:{port}"
            self._engine = create_engine(
                connection_string,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=120,
                connect_args={
                    "read_timeout": 300,
                    "charset": "utf8mb4",
                    "use_unicode": True,
                    "ssl": None,
                    "init_command": f"USE {database}",
                },
            )
            print(f"Database Engine initialized for {database} at {host}")

    @property
    def engine(self):
        if self._engine is None:
            raise RuntimeError(
                f"DatabaseManager '{self}' not initialized. Call initialize() first."
            )
        return self._engine

    def get_df(self, sql: str, params: Optional[dict[str, Any]] = None) -> pd.DataFrame:
        return pd.read_sql(text(sql), con=self.engine, params=params)

    def execute(self, sql: str, params: Optional[dict[str, Any]] = None):
        with self.engine.connect() as conn:
            result = conn.execute(text(sql), params)
            conn.commit()
            return result

    def insert_df(self, df: pd.DataFrame, table_name: str, if_exists: str = "append"):
        df.to_sql(table_name, con=self.engine, if_exists=if_exists, index=False)

    def insert_dict(self, table_name: str, data: dict[str, Any]):
        columns = ", ".join(data.keys())
        placeholders = ", ".join([f":{k}" for k in data.keys()])
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return self.execute(sql, data)

    def dispose(self):
        if self._engine:
            self._engine.dispose()
            self._engine = None

    def dispose_all(self):
        for db in self._instances.values():
            db.dispose()
        self._instances = {}


def get_rpa_db():
    db = DatabaseManager(key="rpa")
    db.initialize(
        settings.DB_USER,
        settings.DB_PASSWORD,
        settings.DB_HOST,
        "rpa",
    )
    return db


def get_glpi_db():
    db = DatabaseManager(key="glpi")
    db.initialize(
        settings.DB_USER,
        settings.DB_PASSWORD,
        settings.DB_HOST,
        "glpi",
    )
    return db
