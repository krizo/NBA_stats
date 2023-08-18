from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float, Boolean

from db.schema.db_team import Base
from db.schema.db_model import Model
from nba_client.api_team_game_stats import ApiTeamGameStats


@dataclass
class TeamGameStats(Base, Model):
    __tablename__ = 'team_stats'

    id: int = Column(Integer(), primary_key=True, autoincrement=True)
    created_at: datetime = Column(DateTime(), default=datetime.now)
    updated_at: datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    game_id: str = Column(String(16), ForeignKey('games.id'))
    team_id: int = Column(Integer(), ForeignKey('teams.id'))
    team: str = Column(String(3))
    opponent_team: str = Column(String(3))
    game_date: datetime = Column(DateTime())
    home_team: str = Column(String(3))
    home_team_id: int = Column(Integer(), ForeignKey('teams.id'))
    away_team_id: int = Column(Integer(), ForeignKey('teams.id'))
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
    minutes: str = Column(String(16))
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
    def create_from_api_model(api_model: ApiTeamGameStats):
        return TeamGameStats(team_id=api_model.team_id, game_id=api_model.game_id, team=api_model.team,
                             game_date=api_model.game_date, home_team_id=api_model.home_team_id,
                             home_team=api_model.home_team, away_team_id=api_model.away_team_id,
                             away_team=api_model.away_team, result=api_model.result, points=api_model.points,
                             opponent_team=api_model.opponent_team, opponent_points=api_model.opponent_points,
                             score=api_model.score, played_at_home=api_model.played_at_home,
                             points_paint=api_model.points_paint, points_2nd_chance=api_model.points_2nd_chance,
                             largest_lead=api_model.largest_lead, lead_changes=api_model.lead_changes,
                             times_tied=api_model.times_tied, minutes=api_model.minutes, fgm=api_model.fgm,
                             fga=api_model.fga, fg_pct=api_model.fg_pct, fg3m=api_model.fg3m, fg3a=api_model.fg3a,
                             fg3_pct=api_model.fg3_pct, ftm=api_model.ftm, ft_pct=api_model.ft_pct, fta=api_model.fta,
                             offensive_rebounds=api_model.offensive_rebounds,
                             defensive_rebounds=api_model.defensive_rebounds, rebounds=api_model.rebounds,
                             assists=api_model.assists, steals=api_model.steals, blocks=api_model.blocks,
                             turnovers=api_model.turnovers, personal_fouls=api_model.personal_fouls,
                             plus_minus=api_model.plus_minus, points_off_to=api_model.points_off_to)
