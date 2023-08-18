from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import declarative_base

from db.db_model import Model
from nba_client.api_team import ApiTeam

Base = declarative_base()


@dataclass
class Team(Base, Model):
    __tablename__ = 'teams'

    id: int = Column(Integer(), primary_key=True, nullable=False, index=True)
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
        from db.database import Database
        return Database.fetch_one(Team, Team.id == team_id)

    @staticmethod
    def create_from_api_model(api_model: ApiTeam):
        return Team(id=api_model.id, name=api_model.name, short_name=api_model.abbreviation,
                    nickname=api_model.nickname, state=api_model.state, city=api_model.city,
                    year_founded=api_model.year_founded)


