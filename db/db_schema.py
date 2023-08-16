from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base

from db.database import Database

Base = declarative_base()


class Model:
    def persist(self):
        from db.database import Database
        Database.insert(self)


@dataclass
class Team(Base, Model):
    __tablename__ = 'teams'

    team_id: int = Column(Integer(), primary_key=True, nullable=False, index=True)
    created_at: datetime = Column(DateTime(), default=datetime.now)
    updated_at: datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    name: str = Column(String(128), nullable=False, index=True)
    short_name: str = Column(String(4), nullable=False)
    nickname: str = Column(String(64), nullable=False)
    city: str = Column(String(64), nullable=False)
    state: str = Column(String(64), nullable=False)
    year_founded: int = Column(Integer())

    @staticmethod
    def fetch_by_id(team_id: int) -> "Team":
        return Database.fetch_one(Team, Team.team_id == team_id)


class Player(Base):
    __tablename__ = 'players'

    player_id = Column(Integer(), primary_key=True)
    team_id = Column(Integer(), ForeignKey('teams.team_id'))
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    first_name = Column(String(128))
    last_name = Column(String(128))
    is_active = Column(Boolean())
    school = Column(String(256))
    birth_date = Column(DateTime())
    age = Column(Integer())
    country = Column(String(16))
    number = Column(Integer())
    weight = Column(Integer())
    height = Column(Integer())
    first_season = Column(Integer())
    draft_year = Column(Integer())
    draft_number = Column(Integer())
