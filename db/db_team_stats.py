from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float, Boolean

from db.db_team import Base
from db.db_model import Model


@dataclass
class TeamStats(Base, Model):
    __tablename__ = 'team_stats'

    id: int = Column(Integer(), primary_key=True)
    created_at: datetime = Column(DateTime(), default=datetime.now)
    updated_at: datetime = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    game_id: int = Column(Integer())
    team_id: int = Column(Integer(), ForeignKey('teams.id'))
    team: str = Column(String(3))
    date: datetime = Column(DateTime())
    home_team: str = Column(String(3))
    away_team_id: int = Column(Integer(), ForeignKey('teams.id'))
    away_team: str = Column(String(3))
    result: str = Column(String(1))
    points: int = Column(Integer())
    opponent_team: str = Column(String(3))
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
    plus_minus: int = Column(Integer())
