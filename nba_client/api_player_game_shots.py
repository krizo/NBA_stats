from datetime import datetime

from nba_api.stats.endpoints import ShotChartDetail
from requests import ReadTimeout
from retry import retry

from nba_client.api_team import ApiTeam
from nba_client.season import Season


class ApiPlayerSeasonShots:
    """ Class representing a player taken from NBA api client """

    def __init__(self, player_id: int, season: Season, shot_details: dict):
        self.player_id = player_id
        self.season = season
        self._shot_details = shot_details

    @property
    def game_id(self) -> str:
        return self._shot_details.get('GAME_ID') if self._shot_details else None

    @property
    def event_id(self) -> int:
        return self._shot_details.get('GAME_EVENT_ID') if self._shot_details else None

    @property
    def team_id(self) -> int:
        return self._shot_details.get('TEAM_ID') if self._shot_details else None

    @property
    def team(self) -> str:
        team = ApiTeam.get_team_by_id(self.team_id)
        return team.get('abbreviation') if team else None

    @property
    def player_name(self) -> str:
        return self._shot_details.get('PLAYER_NAME') if self._shot_details else None

    @property
    def opponent_team(self) -> str or None:
        if self._shot_details:
            home_team = self._shot_details.get('HTM')
            away_team = self._shot_details.get('VTM')
            return home_team if self.team == away_team else away_team
        return None

    @property
    def event_type(self) -> str:
        return self._shot_details.get('EVENT_TYPE') if self._shot_details else None

    @property
    def period(self) -> int:
        return self._shot_details.get('PERIOD') if self._shot_details else None

    @property
    def period_time(self) -> str or None:
        minutes_remaining = self._shot_details.get('MINUTES_REMAINING') if self._shot_details else None
        seconds_remaining = self._shot_details.get('SECONDS_REMAINING') if self._shot_details else None
        if minutes_remaining and seconds_remaining:
            return f"{minutes_remaining}:{seconds_remaining}"
        return None

    @property
    def action_type(self) -> str:
        return self._shot_details.get('ACTION_TYPE') if self._shot_details else None

    @property
    def shot_type(self) -> str:
        return self._shot_details.get('SHOT_TYPE') if self._shot_details else None

    @property
    def shot_zone(self) -> str:
        return self._shot_details.get('SHOT_ZONE_BASIC') if self._shot_details else None

    @property
    def shot_zone_area(self) -> str:
        return self._shot_details.get('SHOT_ZONE_AREA') if self._shot_details else None

    @property
    def shot_zone_range(self) -> str:
        return self._shot_details.get('SHOT_ZONE_RANGE') if self._shot_details else None

    @property
    def shot_distance_feet(self) -> int:
        return self._shot_details.get('SHOT_DISTANCE') if self._shot_details else None

    @property
    def shot_distance_m(self) -> int or None:
        return int(self.shot_distance_feet * 0.3048) if self.shot_distance_feet else None

    @property
    def shot_loc_x(self) -> int:
        return self._shot_details.get('LOC_X') if self._shot_details else None

    @property
    def shot_loc_y(self) -> int:
        return self._shot_details.get('LOC_Y') if self._shot_details else None

    @property
    def shot_successful(self) -> bool:
        return self._shot_details.get('SHOT_MADE_FLAG') == 1 if self._shot_details else None

    @property
    def game_date(self) -> datetime:
        game_date = self._shot_details.get('GAME_DATE') if self._shot_details else None
        return datetime.strptime(game_date, '%Y%m%d') if game_date else None

    @staticmethod
    @retry(exceptions=ReadTimeout, tries=5, delay=10)
    def _get_player_shots_for_game(player_id: int, team_id: int, season: Season):
        response = ShotChartDetail(player_id=player_id, team_id=team_id,
                                   season_nullable=season.name, context_measure_simple='FGA').get_normalized_dict()
        return response['Shot_Chart_Detail'] if response else response

    @classmethod
    @retry(exceptions=ReadTimeout, tries=5, delay=10)
    def fetch_player_shots_records_from_nba(cls, player_id: int, team_id: int, season: Season):
        return  cls._get_player_shots_for_game(player_id=player_id, team_id=team_id, season=season)
