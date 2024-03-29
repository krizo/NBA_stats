from abc import abstractmethod

from nba_api.stats.endpoints import BoxScoreTraditionalV2
from retry import retry

from nba_client.api_client_config import RETRY_DELAY, RETRY_ATTEMPTS
from nba_client.api_game import ApiGame


class ApiGameStatsBase(ApiGame):
    """ Base class for statistics for specific Game"""

    def __init__(self, game_id: str, team_id: int, player_id: int or None):
        super().__init__(game_id)
        self.game_id = game_id
        self._inf = None
        self._stats = None
        self.team_id = team_id
        self.player_id = player_id

    @property
    def _scores(self) -> dict or None:
        if self._box_score_summary:
            return self._box_score_summary.get('LineScore')
        return None

    @property
    def _traditional_stats(self) -> dict:
        if self._stats is None:
            stats = self.get_box_score_tradition(self.game_id)
            self._stats = stats if stats else None
        return self._stats

    @property
    def _team_stats(self) -> dict or None:
        if self._traditional_stats:
            return self._get_team_stats(stats=self._traditional_stats.get('TeamStats'), team_id=self.team_id)
        return None

    @property
    def _opponent_team_stats(self) -> dict or None:
        if self._traditional_stats:
            return self._get_team_stats(stats=self._traditional_stats.get('TeamStats'), team_id=self.opponent_team_id)
        return None

    @property
    def team(self) -> str:
        return self._get_team_short_name(self.team_id)

    @property
    def opponent_team_id(self) -> int:
        if self.home_team_id == self.team_id:
            return self.away_team_id
        return self.home_team_id

    @property
    def opponent_team(self) -> str:
        return self._get_team_short_name(self.opponent_team_id)

    @property
    def team_points(self) -> int:
        return self._team_stats.get('PTS') if self._team_stats else None

    @property
    def opponent_points(self) -> int:
        return self._opponent_team_stats.get('PTS') if self._opponent_team_stats else None

    @property
    @abstractmethod
    def points(self):
        pass

    @property
    def result(self):
        return 'W' if self.points > self.opponent_points else 'L'

    @property
    def played_at_home(self) -> bool:
        return self.home_team_id == self.team_id

    @staticmethod
    @retry(tries=RETRY_DELAY, delay=RETRY_ATTEMPTS)
    def get_box_score_tradition(game_id: str):
        return BoxScoreTraditionalV2(game_id).get_normalized_dict()
