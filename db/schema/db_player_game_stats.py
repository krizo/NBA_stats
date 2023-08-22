from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float, Boolean

from db.schema.db_team import Base
from db.schema.db_model import Model
from helpers.logger import Log
from nba_client.api_player_game_stats import ApiPlayerGameStats
from nba_client.api_team_game_stats import ApiTeamGameStats


@dataclass
class PlayerGameStats(Base, Model):
    __tablename__ = 'player_game_stats'

    id: int = Column(Integer(), primary_key=True, autoincrement=True)
    created_at: datetime = Column(DateTime(), default=datetime.now)
    updated_at: datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    game_id: str = Column(String(16), ForeignKey('games.id'), index=True)
    player_id: int = Column(Integer(), ForeignKey('players.player_id'), index=True)
    team_id: int = Column(Integer(), ForeignKey('teams.team_id'), index=True)
    home_team_id: int = Column(Integer(), ForeignKey('teams.team_id'))
    away_team_id: int = Column(Integer(), ForeignKey('teams.team_id'))
    opponent_team_id: int = Column(Integer(), ForeignKey('teams.team_id'), index=True)
    team: str = Column(String(3))
    opponent_team: str = Column(String(3))
    home_team: str = Column(String(3))
    away_team: str = Column(String(3))
    game_date: datetime = Column(DateTime())
    season: str = Column(String(8))
    team_points: int = Column(Integer())
    player_name: str = Column(String(128))
    score: str = Column(String(8))
    result: str = Column(String(1))
    played_at_home: bool = Column(Boolean)
    points: int = Column(Integer())
    opponent_points: int = Column(Integer())
    fgm: int = Column(Integer())
    fga: int = Column(Integer())
    fg_pct: float = Column(Float())
    fg3m: int = Column(Integer())
    fg3a: int = Column(Integer())
    fg3_pct: float = Column(Float())
    ftm: int = Column(Integer())
    fta: int = Column(Integer())
    ft_pct: float = Column(Float())
    offensive_rebounds: int = Column(Integer())
    defensive_rebounds: int = Column(Integer())
    rebounds: int = Column(Integer())
    assists: int = Column(Integer())
    steals: int = Column(Integer())
    blocks: int = Column(Integer())
    turnovers: int = Column(Integer())
    personal_fouls: int = Column(Integer())
    minutes: int = Column(Integer())
    plus_minus: float = Column(Float())

    @staticmethod
    def create_from_api_model(api_model: ApiPlayerGameStats):
        return PlayerGameStats(player_id=api_model.player_id, team_id=api_model.team_id, game_id=api_model.game_id,
                               team=api_model.team, game_date=api_model.game_date, home_team_id=api_model.home_team_id,
                               home_team=api_model.home_team, away_team_id=api_model.away_team_id,
                               away_team=api_model.away_team, opponent_team_id=api_model.opponent_team_id,
                               season=api_model.season, result=api_model.result, team_points=api_model.team_points,
                               player_name=api_model.player_name, points=api_model.points,
                               opponent_team=api_model.opponent_team, opponent_points=api_model.opponent_points,
                               score=api_model.score, played_at_home=api_model.played_at_home,
                               minutes=api_model.minutes, fgm=api_model.fgm, fga=api_model.fga, fg_pct=api_model.fg_pct,
                               fg3m=api_model.fg3m, fg3a=api_model.fg3a, fg3_pct=api_model.fg3_pct, ftm=api_model.ftm,
                               ft_pct=api_model.ft_pct, fta=api_model.fta,
                               offensive_rebounds=api_model.offensive_rebounds,
                               defensive_rebounds=api_model.defensive_rebounds, rebounds=api_model.rebounds,
                               assists=api_model.assists, steals=api_model.steals, blocks=api_model.blocks,
                               turnovers=api_model.turnovers, personal_fouls=api_model.personal_fouls,
                               plus_minus=api_model.plus_minus)

    @staticmethod
    def fetch(player_id: int, game_id) -> "PlayerGameStats":
        from db.database import Database
        Log.info(f"Fetching {game_id} game performed by player id: {player_id}")
        return Database.fetch_one(PlayerGameStats, PlayerGameStats.player_id == player_id and
                                  PlayerGameStats.game_id == game_id)
