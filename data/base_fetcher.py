import pandas as pd
from pandas import DataFrame
from sqlalchemy import Connection

from db.db_connection import DatabaseConnection


class BaseFetcher:
    _conn = None
    _table_name = None

    @classmethod
    def get_all(cls) -> DataFrame:
        return cls._select_all()

    @classmethod
    def _get_connection(cls) -> Connection:
        if cls._conn is None:
            cls._conn = DatabaseConnection().connection
        return cls._conn

    @classmethod
    def _get_dataframe(cls, query: str) -> DataFrame:
        return pd.read_sql(sql=query, con=cls._get_connection())

    @classmethod
    def _select_all(cls) -> DataFrame:
        return cls._get_dataframe(cls._select_all_query())

    @classmethod
    def _select_all_query(cls) -> str:
        return f"SELECT * FROM {cls._table_name} "

