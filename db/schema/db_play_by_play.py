from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String

from db.schema.db_model import DbModel
from db.schema.db_team import Base
from nba_client.api_play_by_play import ApiPlayByPlay


@dataclass
class PlayByPlay(Base, DbModel):
    __tablename__ = 'play_by_play'
    id: int = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    game_id: str = Column(String(16), ForeignKey('games.id'), index=True)
    home_team_id: int = Column(Integer(), ForeignKey('teams.team_id'), index=True, nullable=True)
    away_team_id: int = Column(Integer(), ForeignKey('teams.team_id'), index=True, nullable=True)
    created_at: datetime = Column(DateTime(), default=datetime.now)
    game_date: datetime = Column(DateTime())
    home_team: str = Column(String(3))
    away_team: str = Column(String(3))
    season: str = Column(String(16))
    season_type: str = Column(String(16))
    event_id: int = Column(Integer())
    event_type: str = Column(String(64))
    event_action_type_id: int = Column(Integer())
    abs_time: str = Column(String(8))
    period_time: str = Column(String(8))
    home_event: str = Column(String(256))
    visitor_event: str = Column(String(256))
    neutral_event: str = Column(String(256))
    score: str = Column(String(16))
    score_margin: str = Column(String(16))
    person_1_type: int = Column(Integer())
    person_1_id: int = Column(Integer())
    person_1_name: str = Column(String(256))
    person_1_team_id: str = Column(Integer(), ForeignKey('teams.team_id'))
    person_1_team: str = Column(String(3))
    person_2_type: int = Column(Integer())
    person_2_id: int = Column(Integer())
    person_2_name: str = Column(String(256))
    person_2_team_id: str = Column(Integer(), ForeignKey('teams.team_id'))
    person_2_team: str = Column(String(3))
    person_3_type: int = Column(Integer())
    person_3_id: int = Column(Integer())
    person_3_name: str = Column(String(256))
    person_3_team_id: str = Column(Integer(), ForeignKey('teams.team_id'))
    person_3_team: str = Column(String(3))

    @staticmethod
    def create_from_api_model(api_model: ApiPlayByPlay):
        return PlayByPlay(game_id=api_model.game_id, game_date=api_model.game_date, home_team_id=api_model.home_team_id,
                          away_team_id=api_model.home_team_id, season=api_model.season, home_team=api_model.home_team,
                          away_team=api_model.away_team,
                          season_type=api_model.season_type, event_id=api_model.event_id, abs_time=api_model.abs_time,
                          period_time=api_model.period_time, event_type=api_model.event_type.name,
                          event_action_type_id=api_model.event_action_type_id, home_event=api_model.home_event,
                          visitor_event=api_model.visitor_event, neutral_event=api_model.neutral_event,
                          score=api_model.score, score_margin=api_model.score_margin, person_1_id=api_model.person_1_id,
                          person_1_name=api_model.person_1_name, person_1_type=api_model.person_1_type,
                          person_1_team=api_model.person_1_team, person_2_id=api_model.person_2_id,
                          person_2_name=api_model.person_2_name, person_2_type=api_model.person_2_type,
                          person_2_team=api_model.person_2_team, person_3_id=api_model.person_3_id,
                          person_3_name=api_model.person_3_name, person_3_type=api_model.person_3_type,
                          person_3_team=api_model.person_3_team
                          )
