from datetime import datetime

from nba_api.stats.endpoints import BoxScoreSummaryV2

from db.schema.db_team import Team
from nba_client.season import Season


class ApiGame:
    """ Class representing a game taken from NBA api client """

    def __init__(self, game_id: str):
        self.game_id = game_id
        self._inf = None

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
    def home_team_id(self) -> int:
        return self._summary.get('HOME_TEAM_ID') if self._summary else None

    @property
    def home_team(self) -> str:
        return Team.fetch_by_id(self.home_team_id).short_name

    @property
    def away_team_id(self) -> int:
        return self._summary.get('VISITOR_TEAM_ID') if self._summary else None

    @property
    def away_team(self) -> str:
        return Team.fetch_by_id(self.away_team_id).short_name

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
        if self.game_date.month < 10:
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
    def _get_team_stats(stats: list[dict], team_id: int) -> dict or None:
        try:
            return next(s for s in stats if s['TEAM_ID'] == team_id)
        except StopIteration:
            return None
