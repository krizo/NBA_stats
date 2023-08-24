from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float, Boolean

from db.schema.db_team import Base
from db.schema.db_model import DbModel
from nba_client.api_team_game_stats import ApiTeamGameStats


@dataclass
class TeamGameStats(Base, DbModel):
    __tablename__ = 'team_game_stats'

    id: str = Column(String(64), primary_key=True, index=True, unique=True)
    created_at: datetime = Column(DateTime(), default=datetime.now)
    updated_at: datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    season_type_id: str = Column(String(3))
    season_type: str = Column(String(32))
    season: str = Column(String(16))
    game_id: str = Column(String(16), ForeignKey('games.id'), index=True)
    team_id: int = Column(Integer(), ForeignKey('teams.team_id'), index=True)
    opponent_team_id: int = Column(Integer(), ForeignKey('teams.team_id'), index=True)
    team: str = Column(String(3))
    opponent_team: str = Column(String(3))
    game_date: datetime = Column(DateTime())
    home_team: str = Column(String(3))
    home_team_id: int = Column(Integer(), ForeignKey('teams.team_id'))
    away_team_id: int = Column(Integer(), ForeignKey('teams.team_id'))
    away_team: str = Column(String(3))
    result: str = Column(String(1))
    points: int = Column(Integer())
    opponent_points: int = Column(Integer())
    score: str = Column(String(8))
    played_at_home: bool = Column(Boolean)
    points_paint: int = Column(Integer())
    points_2nd_chance: int = Column(Integer())
    largest_lead: int = Column(Integer())
    lead_changes: int = Column(Integer())
    times_tied: int = Column(Integer())
    minutes: int = Column(Integer())
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
    plus_minus: float = Column(Float())
    points_off_to: int = Column(Integer())

    @staticmethod
    def fetch(team_id: int, game_id: str) -> "TeamGameStats":
        from db.database import Database
        return Database.fetch_one(TeamGameStats, TeamGameStats.team_id == team_id and TeamGameStats.game_id == game_id)

    @staticmethod
    def create_from_api_model(api_model: ApiTeamGameStats):
        stat_id = f"{api_model.team_id}_{api_model.game_id}"
        return TeamGameStats(id=stat_id, team_id=api_model.team_id, game_id=api_model.game_id, team=api_model.team,
                             game_date=api_model.game_date, home_team_id=api_model.home_team_id,
                             home_team=api_model.home_team, away_team_id=api_model.away_team_id,
                             season_type_id=api_model.season_type_id, season_type=api_model.season_type,
                             away_team=api_model.away_team, result=api_model.result, points=api_model.points,
                             opponent_team=api_model.opponent_team, opponent_points=api_model.opponent_points,
                             opponent_team_id=api_model.opponent_team_id, score=api_model.score,
                             played_at_home=api_model.played_at_home, minutes=api_model.minutes, fgm=api_model.fgm,
                             largest_lead=api_model.largest_lead, lead_changes=api_model.lead_changes,
                             fga=api_model.fga, fg_pct=api_model.fg_pct, fg3m=api_model.fg3m, fg3a=api_model.fg3a,
                             fg3_pct=api_model.fg3_pct, ftm=api_model.ftm, ft_pct=api_model.ft_pct, fta=api_model.fta,
                             times_tied=api_model.times_tied, offensive_rebounds=api_model.offensive_rebounds,
                             points_paint=api_model.points_paint, points_2nd_chance=api_model.points_2nd_chance,
                             points_off_to=api_model.points_off_to, defensive_rebounds=api_model.defensive_rebounds,
                             rebounds=api_model.rebounds, assists=api_model.assists, steals=api_model.steals,
                             blocks=api_model.blocks, turnovers=api_model.turnovers, season=api_model.season,
                             personal_fouls=api_model.personal_fouls, plus_minus=api_model.plus_minus, )
