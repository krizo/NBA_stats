from typing import Any

from psycopg2 import IntegrityError, ProgrammingError
from sqlalchemy import BinaryExpression, inspect, text
from sqlalchemy.orm import Session
from sqlalchemy.orm.base import instance_dict

from helpers.logger import Log


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
        insp = inspect(cls.get_engine())
        for table_entry in reversed(insp.get_sorted_table_and_fkc_names()):
            table_name = table_entry[0]
            if table_name:
                with cls.get_engine().begin() as conn:
                    conn.execute(text(f'DROP TABLE "{table_name}"'))

    @classmethod
    def create_tables(cls):
        from db.db_schema import Base
        Base.metadata.create_all(cls.get_engine())

    @classmethod
    def drop_table(cls, klass: "Base"):
        try:
            klass.__table__.drop(cls.get_engine())
        except Exception:
            Log.warning(f"Table {klass.__table__} doesn't exist")

    @classmethod
    def create_table(cls, klass: "Base"):
        try:
            klass.__table__.create(cls.get_engine())
        except Exception:
            Log.warning(f"Table {klass.__table__} already exists")

    @classmethod
    def insert(cls, record: Any):
        with Session(cls.get_engine()) as session:
            session.add(record)
            try:
                session.commit()
            except Exception as ex:
                if ex.orig.pgcode == 23505:
                    Log.warning(f"Record {record.id} already exists in {record.__table__}")
            session.flush()

    @classmethod
    def update(cls, existing_object: object, updated_object: object):
        with Session(cls.get_engine()) as session:
            existing_record = session.query(type(existing_object)).get(existing_object.id)
            if existing_record:
                for key, value in instance_dict(updated_object).items():
                    setattr(existing_record, key, value)
            session.commit()

    @classmethod
    def fetch_one(cls, model: object, kwargs):
        with Session(cls.get_engine()) as session:
            query = session.query(model)
            return query.filter(kwargs).first()

    @classmethod
    def fetch_all(cls, klass: object, kwargs):
        with Session(cls.get_engine()) as session:
            query = session.query(klass)
            return query.filter(kwargs).all()
