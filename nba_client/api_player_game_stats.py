from datetime import datetime

from nba_api.stats.endpoints import leaguegamefinder, BoxScoreSummaryV2, BoxScoreTraditionalV2, boxscoreplayertrackv2

from nba_client.api_game_stats_base_py import ApiGameStatsBase
from nba_client.season import Season


class ApiPlayerGameStats(ApiGameStatsBase):
    """ Class representing a game stats for specific player taken from NBA api client """

    def __init__(self, game_id: str, player_id: int):
        self._team_id = None
        self.game_id = game_id
        self.player_id = player_id
        super().__init__(game_id=game_id, player_id=player_id, team_id=self.team_id)

    @property
    def _player_stats(self) -> dict or None:
        if self._traditional_stats:
            return self._get_player_stats(self._traditional_stats.get('PlayerStats'))
        return None

    @property
    def _team_ids(self) -> tuple:
        team_stats = self._traditional_stats.get('TeamStats')
        return team_stats[0].get('TEAM_ID'), team_stats[1].get('TEAM_ID')

    @property
    def team(self) -> str:
        return self._player_stats.get('TEAM_ABBREVIATION') if self._player_stats else None

    @property
    def team_id(self):
        return self._team_id

    @team_id.setter
    def team_id(self, team_id):
        self._team_id = int(self._player_stats.get('TEAM_ID')) if self._player_stats else None

    @property
    def player_name(self):
        return self._player_stats.get('PLAYER_NAME')

    @property
    def minutes(self) -> int:
        minutes = self._player_stats.get('MIN') if self._player_stats else None
        return int(float(minutes.split(':')[0]))

    @property
    def fgm(self) -> int:
        return self._player_stats.get('FGM') if self._player_stats else None

    @property
    def fga(self) -> int:
        return self._player_stats.get('FGA') if self._player_stats else None

    @property
    def fg_pct(self) -> float:
        return self._player_stats.get('FG_PCT') if self._player_stats else None

    @property
    def fg3m(self) -> int:
        return self._player_stats.get('FG3M') if self._player_stats else None

    @property
    def fg3a(self) -> int:
        return self._player_stats.get('FG3A') if self._player_stats else None

    @property
    def fg3_pct(self) -> float:
        return self._player_stats.get('FG3_PCT') if self._player_stats else None

    @property
    def ftm(self) -> int:
        return self._player_stats.get('FTM') if self._player_stats else None

    @property
    def fta(self) -> int:
        return self._player_stats.get('FTA') if self._player_stats else None

    @property
    def ft_pct(self) -> float:
        return self._player_stats.get('FT_PCT') if self._player_stats else None

    @property
    def offensive_rebounds(self) -> int:
        return self._player_stats.get('OREB') if self._player_stats else None

    @property
    def defensive_rebounds(self) -> int:
        return self._player_stats.get('DREB') if self._player_stats else None

    @property
    def rebounds(self) -> int:
        return self._player_stats.get('REB') if self._player_stats else None

    @property
    def assists(self) -> int:
        return self._player_stats.get('AST') if self._player_stats else None

    @property
    def steals(self) -> int:
        return self._player_stats.get('STL') if self._player_stats else None

    @property
    def blocks(self) -> int:
        return self._player_stats.get('BLK') if self._player_stats else None

    @property
    def turnovers(self) -> int:
        return self._player_stats.get('TO') if self._player_stats else None

    @property
    def personal_fouls(self) -> int:
        return self._player_stats.get('PF') if self._player_stats else None

    @property
    def points(self) -> int:
        return self._player_stats.get('PTS') if self._player_stats else None

    @property
    def opponent_points(self) -> int:
        return self._opponent_team_stats.get('PTS') if self._opponent_team_stats else None

    @property
    def plus_minus(self) -> float:
        return self._player_stats.get('PLUS_MINUS') if self._player_stats else None

    @property
    def result(self):
        return 'W' if self.points > self.opponent_points else 'L'

    @property
    def score(self) -> str:
        return f"{self.team_points}:{self.opponent_points}"

    def _get_player_stats(self, stats: list[dict]) -> dict or None:
        try:
            return next(s for s in stats if s['PLAYER_ID'] == self.player_id)
        except StopIteration:
            return None

