from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import declarative_base

from db.schema.db_model import DbModel
from nba_client.api_team import ApiTeam

Base = declarative_base()


@dataclass
class Team(Base, DbModel):
    __tablename__ = 'teams'

    team_id: int = Column(Integer(), primary_key=True, nullable=False, index=True)
    created_at: datetime = Column(DateTime(), default=datetime.now)
    updated_at: datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    name: str = Column(String(128), nullable=False, index=True)
    abbreviation: str = Column(String(4), nullable=False)
    nickname: str = Column(String(64), nullable=False)
    city: str = Column(String(64), nullable=False)
    state: str = Column(String(64), nullable=False)
    year_founded: int = Column(Integer())

    @staticmethod
    def fetch_by_id(team_id: int) -> "Team":
        from db.database import Database
        return Database.fetch_one(Team, Team.team_id == team_id)

    @staticmethod
    def fetch_all() -> ["Team"]:
        from db.database import Database
        return Database.fetch_all(Team)

    @staticmethod
    def fetch_by_name(name: str):
        from db.database import Database
        return Database.fetch_one(Team, Team.name == name)

    @staticmethod
    def fetch_by_short_name(short_name: str):
        from db.database import Database
        return Database.fetch_one(Team, Team.abbreviation == short_name)

    @staticmethod
    def create_from_api_model(api_model: ApiTeam):
        return Team(team_id=api_model.team_id, name=api_model.name, abbreviation=api_model.abbreviation,
                    nickname=api_model.nickname, state=api_model.state, city=api_model.city,
                    year_founded=api_model.year_founded)
