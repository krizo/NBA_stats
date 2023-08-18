from typing import Any

from sqlalchemy import create_engine, Engine, Connection
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, Session

from db.db_credentials import DbCredentials
from db.db_team import Base


class DatabaseConnection:
    _conn = None
    _sess = None

    def __init__(self):
        credentials = DbCredentials()
        self.url = URL.create(
            drivername=credentials.driver,
            username=credentials.user_name,
            password=credentials.password,
            host=credentials.hostname,
            port=credentials.port,
            database=credentials.db_name
        )

    @property
    def engine(self) -> Engine:
        return create_engine(self.url)

    @property
    def _connection(self) -> Connection:
        if self._conn is None:
            self._conn = self.engine.connect()
        return self._conn
