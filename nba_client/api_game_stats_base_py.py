from datetime import datetime

from nba_api.stats.endpoints import BoxScoreTraditionalV2, BoxScoreSummaryV2

from db.schema.db_team import Team


class ApiGameStatsBase:
    """ Base class for statistics for specific Game"""

    def __init__(self, game_id: str, team_id: int, player_id: int or None):
        self.game_id = game_id
        self._inf = None
        self._stats = None
        self.team_id = team_id
        self.player_id = player_id

    @property
    def _box_score_summary(self) -> dict:
        if self._inf is None:
            self._inf = BoxScoreSummaryV2(game_id=self.game_id).get_normalized_dict()
        return self._inf

    @property
    def _summary(self) -> dict:
        return self._box_score_summary.get('GameSummary')[0]

    @property
    def _game_info(self) -> dict:
        data = self._box_score_summary.get('GameInfo')
        return data[0] if data else None

    @property
    def _scores(self) -> dict or None:
        if self._box_score_summary:
            return self._box_score_summary.get('LineScore')
        return None

    @property
    def _traditional_stats(self) -> dict:
        if self._stats is None:
            stats = BoxScoreTraditionalV2(self.game_id)
            self._stats = stats.get_normalized_dict() if stats else None
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
    def _other_stats(self) -> dict or None:
        if self._box_score_summary:
            return self._get_team_stats(stats=self._box_score_summary.get('OtherStats'), team_id=self.team_id)
        return None

    @property
    def team(self) -> str:
        return Team.fetch_by_id(self.team_id).short_name

    @property
    def opponent_team_id(self) -> int:
        if self.home_team_id == self.team_id:
            return self.away_team_id
        return self.home_team_id

    @property
    def opponent_team(self) -> str:
        return Team.fetch_by_id(self.opponent_team_id).short_name

    @property
    def home_team_id(self) -> int:
        return self._summary.get('HOME_TEAM_ID') if self._summary else None

    @property
    def home_team(self) -> str:
        return Team.fetch_by_id(self.home_team_id).short_name if self.home_team_id else None

    @property
    def away_team_id(self) -> int:
        return self._summary.get('VISITOR_TEAM_ID') if self._summary else None

    @property
    def team_points(self) -> int:
        return self._team_stats.get('PTS') if self._team_stats else None

    @property
    def away_team(self) -> str:
        return Team.fetch_by_id(self.away_team_id).short_name if self.away_team_id else None

    @property
    def game_date(self) -> datetime or None:
        date_str = self._summary.get('GAME_DATE_EST') if self._summary else None
        if date_str:
            return datetime.strptime(date_str.rpartition('T')[0], "%Y-%m-%d")
        return None

    @property
    def opponent_points(self) -> int:
        return self._opponent_team_stats.get('PTS') if self._opponent_team_stats else None

    @property
    def result(self):
        return 'W' if self.points > self.opponent_points else 'L'

    @property
    def played_at_home(self) -> bool:
        return self.home_team_id == self.team_id

    @staticmethod
    def _get_team_stats(stats: list[dict], team_id: int = None) -> dict or None:
        try:
            return next(s for s in stats if s['TEAM_ID'] == team_id)
        except StopIteration:
            return None
