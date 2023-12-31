from sqlalchemy import create_engine, Engine, Connection
from sqlalchemy.engine import URL

from db.db_credentials import DbCredentials


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
    def connection(self) -> Connection:
        if self._conn is None:
            self._conn = self.engine.connect()
        return self._conn
