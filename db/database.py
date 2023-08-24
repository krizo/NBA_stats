from typing import Any

from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.orm.base import instance_dict

from db.schema.db_game import Game
from db.schema.db_player_game_stats import PlayerGameStats
from db.schema.db_team_game_stats import TeamGameStats
from db.schema.db_player import Player
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
        from db.schema.db_team import Team
        for table in [Team, Player, Game, TeamGameStats, PlayerGameStats]:
            cls.create_table(table)

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
        except Exception as ex:
            Log.warning(f"Table {klass.__table__} already exists")

    @classmethod
    def insert(cls, record: Any):
        with Session(cls.get_engine()) as session:
            session.add(record)
            try:
                session.commit()
            except IntegrityError as ex:
                Log.warning(f"Can't insert record into {record.__table__}. {ex}")
                session.flush()
                return
            except Exception as ex:
                Log.error(f"Can't insert record {record}.")
                for ex_arg in ex.args:
                    Log.error(f"\t{ex_arg}")

    @classmethod
    def update(cls, existing_object: object, updated_object: object, primary_key: str):
        with Session(cls.get_engine()) as session:
            existing_record = session.query(type(existing_object)).get(existing_object.__getattribute__(primary_key))
            if existing_record:
                for key, value in instance_dict(updated_object).items():
                    setattr(existing_record, key, value)
            session.commit()

    @classmethod
    def fetch_one(cls, model: object, *args):
        with Session(cls.get_engine()) as session:
            query = session.query(model)
            return query.filter(*args).first()

    @classmethod
    def fetch_all(cls, klass: object):
        with Session(cls.get_engine()) as session:
            return session.query(klass).all()