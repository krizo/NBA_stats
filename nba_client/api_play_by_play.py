import re
from datetime import datetime
from json import JSONDecodeError

from nba_api.stats.endpoints import PlayByPlayV2, PlayByPlay
from nba_api.stats.library.eventmsgtype import EventMsgType
from requests import ReadTimeout
from retry import retry

from helpers.logger import Log
from nba_client.api_client_config import RETRY_ATTEMPTS, RETRY_DELAY
from nba_client.season import Season
from nba_client.season_type import SeasonType


class ApiPlayByPlay:
    _cached_data = {}

    def __init__(self, game_id: str, play_by_play: dict, game_date: datetime, home_team_id: int, away_team_id: int,
                 home_team: str, away_team: str):
        self._play_by_play = play_by_play
        self.game_id = game_id
        self.game_date = game_date
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.home_team = home_team
        self.away_team = away_team

    @property
    def period(self) -> int:
        return self._play_by_play.get('PERIOD')

    @property
    def event_id(self) -> int:
        return self._play_by_play.get('EVENTNUM')

    @property
    def event_type(self) -> EventMsgType:
        event_type = self._play_by_play.get('EVENTMSGTYPE')
        return EventMsgType(event_type) if event_type else EventMsgType.UNKNOWN

    @property
    def event_action_type_id(self) -> int:
        action_type_id = self._play_by_play.get('EVENTMSGACTIONTYPE')
        return int(action_type_id) if action_type_id else None

    @property
    def abs_time(self) -> str:
        return self._play_by_play.get('WCTIMESTRING')

    @property
    def period_time(self) -> str:
        return self._play_by_play.get('PCTIMESTRING')

    @property
    def home_event(self) -> str:
        return self._play_by_play.get('HOMEDESCRIPTION')

    @property
    def visitor_event(self) -> str:
        return self._play_by_play.get('VISITORDESCRIPTION')

    @property
    def neutral_event(self) -> str:
        return self._play_by_play.get('NEUTRALDESCRIPTION')

    @property
    def score(self) -> str:
        return self._play_by_play.get('SCORE')

    @property
    def score_margin(self) -> str:
        return self._play_by_play.get('SCOREMARGIN')

    @property
    def person_1_type(self) -> int:
        person_type = self._play_by_play.get('PERSON1TYPE')
        return int(person_type) if person_type else person_type

    @property
    def person_1_id(self) -> int:
        person_id = self._play_by_play.get('PLAYER1_ID')
        return int(person_id) if person_id else None

    @property
    def person_1_name(self) -> str:
        return self._play_by_play.get('PLAYER1_NAME')

    @property
    def person_1_team_id(self) -> int:
        return self._play_by_play.get('PLAYER1_TEAM_ID')

    @property
    def person_1_team(self) -> str:
        return self._play_by_play.get('PLAYER1_TEAM_ABBREVIATION')

    @property
    def person_2_type(self) -> int:
        return self._play_by_play.get('PERSON2TYPE')

    @property
    def person_2_id(self) -> int:
        person_id = self._play_by_play.get('PLAYER2_ID')
        return int(person_id) if person_id else None

    @property
    def person_2_name(self) -> str:
        return self._play_by_play.get('PLAYER2_NAME')

    @property
    def person_2_team_id(self) -> int:
        return self._play_by_play.get('PLAYER2_TEAM_ID')

    @property
    def person_2_team(self) -> str:
        return self._play_by_play.get('PLAYER2_TEAM_ABBREVIATION')

    @property
    def person_3_type(self) -> int:
        return self._play_by_play.get('PERSON3TYPE')

    @property
    def person_3_id(self) -> int:
        person_id = self._play_by_play.get('PLAYER3_ID')
        return int(person_id) if person_id else None

    @property
    def person_3_name(self) -> str:
        return self._play_by_play.get('PLAYER3_NAME')

    @property
    def person_3_team_id(self) -> int:
        return self._play_by_play.get('PLAYER3_TEAM_ID')

    @property
    def person_3_team(self) -> str:
        return self._play_by_play.get('PLAYER3_TEAM_ABBREVIATION')

    @property
    def season_type_id(self) -> str:
        return self.game_id[:3]

    @property
    def season_type(self) -> str:
        return str(SeasonType(self.season_type_id))

    @property
    def season(self) -> str:
        if self.game_date.month < 9:
            return Season(self.game_date.year - 1).name
        return Season(self.game_date.year).name

    @classmethod
    def clean_cache(cls, game_id):
        cls._cached_data.pop(game_id)

    @classmethod
    def create_play_by_play_records(cls, game_id: str, game_date: datetime, home_team_id: int,
                                    away_team_id: int, home_team: str, away_team: str) -> ["ApiPlayByPlay"]:
        return [
            ApiPlayByPlay(game_id=game_id, game_date=game_date, home_team_id=home_team_id, away_team_id=away_team_id,
                          play_by_play=pbp, home_team=home_team, away_team=away_team) for pbp in
            cls.fetch_play_by_play_records_from_nba(game_id)]

    @staticmethod
    def _make_play_by_play_request(game_id: str):
        @retry(exceptions=(ReadTimeout, ConnectionError), tries=RETRY_ATTEMPTS, delay=RETRY_DELAY)
        def _make_play_by_play_request_v1():
            return PlayByPlay(game_id=game_id).get_normalized_dict()

        @retry(exceptions=(ReadTimeout, ConnectionError), tries=RETRY_ATTEMPTS, delay=RETRY_DELAY)
        def _make_play_by_play_request_v2():
            return PlayByPlayV2(game_id=game_id).get_normalized_dict()

        try:
            return _make_play_by_play_request_v2()
        except JSONDecodeError:
            try:
                return _make_play_by_play_request_v1()
            except JSONDecodeError:
                Log.warning(f"Can't fetch play by play stats for game {game_id}.")
                return None

    @classmethod
    def fetch_play_by_play_records_from_nba(cls, game_id) -> [dict]:
        cached_data = cls._cached_data.get(game_id)
        if cached_data:
            return cached_data
        pbp_response = cls._make_play_by_play_request(game_id)
        if pbp_response is None:
            raise ValueError(f"No PlayByPlay for game {game_id}")
        Log.info(f"\t\tFetched PlayByPlay record for game {game_id} from NBA stats")
        pbp = pbp_response.get('PlayByPlay')
        cls._cached_data.setdefault(game_id, pbp)
        return cls._cached_data.get(game_id)
