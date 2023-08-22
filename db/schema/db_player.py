from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean

from db.schema.db_model import Model
from db.schema.db_team import Base
from helpers.logger import Log
from nba_client.api_player import ApiPlayer


@dataclass
class Player(Base, Model):
    __tablename__ = 'players'

    player_id: int = Column(Integer(), primary_key=True, index=True)
    team_id: int = Column(Integer(), ForeignKey('teams.team_id'), index=True)
    created_at: datetime = Column(DateTime(), default=datetime.now)
    updated_at: datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    first_name: str = Column(String(128))
    last_name: str = Column(String(128))
    is_active: bool = Column(Boolean())
    school: str = Column(String(256))
    birth_date: datetime = Column(DateTime())
    age: int = Column(Integer())
    country: str = Column(String(16))
    current_number: int = Column(Integer())
    current_team_abbreviation: str = Column(String(3))
    weight: int = Column(Integer())
    height: int = Column(Integer())
    first_season_played: int = Column(Integer())
    draft_year: str = Column(String(16))
    draft_number: str = Column(String(16))

    @staticmethod
    def create_from_api_model(api_model: ApiPlayer):
        return Player(player_id=api_model.player_id, team_id=api_model.current_team_id, first_name=api_model.first_name,
                      last_name=api_model.last_name, is_active=api_model.is_active, school=api_model.school,
                      birth_date=api_model.birth_date, age=api_model.age, country=api_model.country,
                      current_number=api_model.current_number, weight=api_model.weight, height=api_model.height,
                      first_season_played=api_model.first_season_played, draft_year=api_model.draft_year,
                      draft_number=api_model.draft_number,
                      current_team_abbreviation=api_model.current_team_abbreviation)

    @staticmethod
    def fetch_by_id(player_id: int) -> "Player":
        from db.database import Database
        Log.info(f"Fetching player by id: {player_id}")
        return Database.fetch_one(Player, Player.player_id == player_id)
