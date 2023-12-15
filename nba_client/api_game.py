import functools
from datetime import datetime

from nba_api.stats.endpoints import BoxScoreSummaryV2, leaguegamefinder
from retry import retry

from helpers.logger import Log
from nba_client.api_client_config import RETRY_ATTEMPTS, RETRY_DELAY
from nba_client.season import Season
from nba_client.season_type import SeasonType


class ApiGame:
    """ Class representing a game taken from NBA api client """

    def __init__(self, game_id: str):
        self.game_id = game_id
        self._inf = None

    @property
    def season_type_id(self) -> str:
        return self.game_id[:3]

    @property
    def season_type(self) -> str:
        return str(SeasonType(self.season_type_id))

    @property
    def _box_score_summary(self) -> dict:
        if self._inf is None:
            self._inf = self._get_box_score_summary_v2(game_id=self.game_id)
        return self._inf

    @property
    def _summary(self) -> dict:
        return self._box_score_summary.get('GameSummary')[0]

    @property
    def _game_info(self) -> dict:
        data = self._box_score_summary.get('GameInfo')
        return data[0] if data else None

    @property
    def _other_stats(self) -> dict or None:
        if self._box_score_summary:
            return self._box_score_summary.get('OtherStats')
        return None

    @property
    def home_team_id(self) -> int:
        return self._summary.get('HOME_TEAM_ID') if self._summary else None

    @property
    def home_team(self) -> str:
        return self._get_team_short_name(self.home_team_id)

    @property
    def away_team_id(self) -> int:
        return self._summary.get('VISITOR_TEAM_ID') if self._summary else None

    @property
    def away_team(self) -> str:
        return self._get_team_short_name(self.away_team_id)

    def _get_team_short_name(self, team_id):
        other_stats = self._get_team_stats(stats=self._other_stats, team_id=team_id)
        if not other_stats:
            Log.warning(f"Can't find team short name by id: {team_id}")
        return other_stats.get('TEAM_ABBREVIATION') if other_stats else None

    @property
    def _scores(self) -> dict or None:
        if self._box_score_summary:
            return self._box_score_summary.get('LineScore')
        return None

    @property
    def game_date(self) -> datetime or None:
        date_str = self._summary.get('GAME_DATE_EST') if self._summary else None
        if date_str:
            return datetime.strptime(date_str.rpartition('T')[0], "%Y-%m-%d")
        return None

    @property
    def season(self) -> str:
        if self.game_date.month < 9:
            return Season(self.game_date.year - 1).name
        return Season(self.game_date.year).name

    @property
    def matchup(self) -> str:
        return f"{self.away_team}:{self.home_team}"

    @property
    def attendance(self) -> int:
        return self._game_info.get('ATTENDANCE') if self._game_info else None

    @property
    def home_team_points(self) -> int:
        scores = self._get_team_stats(self._scores, self.home_team_id)
        return scores.get('PTS') if scores else None

    @property
    def away_team_points(self) -> int:
        scores = self._get_team_stats(self._scores, self.away_team_id)
        return scores.get('PTS') if scores else None

    @property
    def score(self) -> str:
        return f"{self.away_team_points}:{self.home_team_points}"

    @property
    def status(self) -> str:
        return self._summary.get('GAME_STATUS_TEXT') if self._summary else None

    @property
    def winner(self) -> str:
        if self.home_team_points > self.away_team_points:
            return self.home_team
        return self.away_team

    @staticmethod
    def get_latest_game_persisted() -> "Game":
        from db.schema.db_game import Game
        return Game.fetch_latest_match()

    @staticmethod
    @retry(tries=RETRY_DELAY, delay=RETRY_ATTEMPTS)
    @functools.lru_cache(maxsize=1)
    def get_games(season: Season) -> [dict]:
        game_finder = leaguegamefinder.LeagueGameFinder(season_nullable=season.name, league_id_nullable='00')
        return game_finder.get_normalized_dict().get('LeagueGameFinderResults')



    @staticmethod
    def _get_team_stats(stats: [dict], team_id: int) -> dict or None:
        try:
            return next(s for s in stats if s['TEAM_ID'] == team_id)
        except StopIteration:
            return None

    @staticmethod
    @retry(tries=RETRY_DELAY, delay=RETRY_ATTEMPTS)
    def _get_box_score_summary_v2(game_id: str):
        return BoxScoreSummaryV2(game_id=game_id).get_normalized_dict()
