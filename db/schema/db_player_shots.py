from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Boolean

from db.schema.db_model import DbModel
from db.schema.db_team import Base
from nba_client.api_player_game_shots import ApiPlayerSeasonShots


@dataclass
class PlayerShots(Base, DbModel):
    __tablename__ = 'player_shots'

    id: str = Column(Integer(), primary_key=True, index=True, autoincrement=True)
    created_at: datetime = Column(DateTime(), default=datetime.now)
    player_id: int = Column(Integer(), ForeignKey('players.player_id'), index=True)
    player_name: str = Column(String(128))
    game_id: str = Column(String(16), ForeignKey('games.id'), index=True)
    team_id: int = Column(Integer(), ForeignKey('teams.team_id'), index=True)
    season: str = Column(String(16))
    team: str = Column(String(3))
    opponent_team: str = Column(String(3))
    game_date: datetime = Column(DateTime())
    event_id: int = Column(Integer())
    event_type: str = Column(String(64))
    shot_type: str = Column(String(64))
    shot_successful: bool = Column(Boolean)
    period: int = Column(Integer())
    period_time: str = Column(String(8))
    shot_distance_feet: int = Column(Integer)
    shot_distance_m: int = Column(Integer)
    shot_loc_x: int = Column(Integer)
    shot_loc_y: int = Column(Integer)
    shot_zone: str = Column(String(64))
    shot_zone_area: str = Column(String(64))
    shot_zone_range: str = Column(String(64))

    @staticmethod
    def create_from_api_model(api_model: ApiPlayerSeasonShots) -> "PlayerShots":
        return PlayerShots(player_id=api_model.player_id, player_name=api_model.player_name, game_id=api_model.game_id,
                           team_id=api_model.team_id, team=api_model.team, opponent_team=api_model.opponent_team,
                           game_date=api_model.game_date, event_id=api_model.event_id, event_type=api_model.event_type,
                           shot_type=api_model.shot_type, shot_successful=api_model.shot_successful,
                           period=api_model.period, period_time=api_model.period_time,
                           shot_distance_feet=api_model.shot_distance_feet, shot_distance_m=api_model.shot_distance_m,
                           shot_loc_x=api_model.shot_loc_x, shot_loc_y=api_model.shot_loc_y,
                           shot_zone=api_model.shot_zone, shot_zone_area=api_model.shot_zone_area,
                           shot_zone_range=api_model.shot_zone_range, season=api_model.season.name)
