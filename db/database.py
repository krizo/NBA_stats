from typing import Any

from sqlalchemy import BinaryExpression
from sqlalchemy.orm import Session


class Database:
    _engine = None

    @classmethod
    def get_engine(cls):
        if cls._engine is None:
            from db.db_connection import DatabaseConnection
            cls._engine = DatabaseConnection().engine
        return cls._engine

    @classmethod
    def recreate_database(cls):
        cls.drop_tables()
        cls.create_tables()

    @classmethod
    def drop_tables(cls):
        from db.db_schema import Base
        Base.metadata.drop_all(cls.get_engine())

    @classmethod
    def create_tables(cls):
        from db.db_schema import Base
        Base.metadata.create_all(cls.get_engine())

    @classmethod
    def insert(cls, record: Any):
        with Session(cls.get_engine()) as session:
            session.add(record)
            session.commit()
            session.flush()

    @classmethod
    def fetch_one(cls, klass: object, kwargs):
        with Session(cls.get_engine()) as session:
            query = session.query(klass)
            return query.filter(kwargs).first()

    @classmethod
    def fetch_all(cls, klass: object, kwargs):
        with Session(cls.get_engine()) as session:
            query = session.query(klass)
            return query.filter(kwargs).all()
