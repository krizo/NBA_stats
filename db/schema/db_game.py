from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String

from db.schema.db_team import Base
from db.schema.db_model import DbModel
from nba_client.api_game import ApiGame


@dataclass
class Game(Base, DbModel):
    __tablename__ = 'games'

    id: str = Column(String(16), primary_key=True, index=True)
    created_at: datetime = Column(DateTime(), default=datetime.now)
    game_date: datetime = Column(DateTime())
    season_type_id: str = Column(String(3))
    season_type: str = Column(String(32))
    season: str = Column(String(16))
    home_team_id: int = Column(Integer(), ForeignKey('teams.team_id'), index=True)
    away_team_id: int = Column(Integer(), ForeignKey('teams.team_id'), index=True)
    home_team: str = Column(String(3))
    away_team: str = Column(String(3))
    home_team_points: int = Column(Integer())
    away_team_points: int = Column(Integer())
    matchup: str = Column(String(16))
    score: str = Column(String(8))
    status: str = Column(String(16))
    winner: str = Column(String(3))
    attendance: int = Column(Integer())

    @staticmethod
    def fetch_by_id(game_id: str) -> "Game":
        from db.database import Database
        return Database.fetch_one(Game, Game.id == game_id)

    @staticmethod
    def create_from_api_model(api_model: ApiGame):
        return Game(id=api_model.game_id, game_date=api_model.game_date, season_type_id=api_model.season_type_id,
                    season_type=api_model.season_type, season=api_model.season, home_team_id=api_model.home_team_id,
                    away_team_id=api_model.away_team_id, home_team=api_model.home_team, away_team=api_model.away_team,
                    home_team_points=api_model.home_team_points, away_team_points=api_model.away_team_points,
                    matchup=api_model.matchup, score=api_model.score, status=api_model.status, winner=api_model.winner,
                    attendance=api_model.attendance)
