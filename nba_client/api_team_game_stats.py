import functools
from datetime import datetime

from nba_api.stats.endpoints import leaguegamefinder
from retry import retry

from nba_client.api_client_config import RETRY_DELAY, RETRY_ATTEMPTS
from nba_client.api_game_stats_base import ApiGameStatsBase
from nba_client.season import Season


class ApiTeamGameStats(ApiGameStatsBase):
    """ Class representing a game stats for specific team taken from NBA api client """

    def __init__(self, game_id: str, team_id: int):
        self.game_id = game_id
        super().__init__(game_id=game_id, team_id=team_id, player_id=None)

    @property
    def points_paint(self) -> int:
        return self._other_team_stats.get('PTS_PAINT') if self._other_stats else None

    @property
    def points_2nd_chance(self) -> int:
        return self._other_team_stats.get('PTS_2ND_CHANCE') if self._other_stats else None

    @property
    def _other_team_stats(self):
        return self._get_team_stats(stats=self._box_score_summary.get('OtherStats'), team_id=self.team_id)

    @property
    def largest_lead(self) -> int:
        return self._other_team_stats.get('LARGEST_LEAD') if self._other_team_stats else None

    @property
    def lead_changes(self) -> int:
        return self._other_team_stats.get('LEAD_CHANGES') if self._other_team_stats else None

    @property
    def times_tied(self) -> int:
        return self._other_team_stats.get('TIMES_TIED') if self._other_team_stats else None

    @property
    def points_off_to(self) -> int:
        """ The number of points scored by a team following an opponent's turnover """
        return self._other_team_stats.get('PTS_OFF_TO') if self._other_team_stats else None

    @property
    def minutes(self) -> int:
        minutes = self._team_stats.get('MIN') if self._team_stats else None
        return int(float(minutes.split(':')[0]))

    @property
    def fgm(self) -> int:
        return self._team_stats.get('FGM') if self._team_stats else None

    @property
    def fga(self) -> int:
        return self._team_stats.get('FGA') if self._team_stats else None

    @property
    def fg_pct(self) -> float:
        return self._team_stats.get('FG_PCT') if self._team_stats else None

    @property
    def fg3m(self) -> int:
        return self._team_stats.get('FG3M') if self._team_stats else None

    @property
    def fg3a(self) -> int:
        return self._team_stats.get('FG3A') if self._team_stats else None

    @property
    def fg3_pct(self) -> float:
        return self._team_stats.get('FG3_PCT') if self._team_stats else None

    @property
    def ftm(self) -> int:
        return self._team_stats.get('FTM') if self._team_stats else None

    @property
    def fta(self) -> int:
        return self._team_stats.get('FTA') if self._team_stats else None

    @property
    def ft_pct(self) -> float:
        return self._team_stats.get('FT_PCT') if self._team_stats else None

    @property
    def offensive_rebounds(self) -> int:
        return self._team_stats.get('OREB') if self._team_stats else None

    @property
    def defensive_rebounds(self) -> int:
        return self._team_stats.get('DREB') if self._team_stats else None

    @property
    def rebounds(self) -> int:
        return self._team_stats.get('REB') if self._team_stats else None

    @property
    def assists(self) -> int:
        return self._team_stats.get('AST') if self._team_stats else None

    @property
    def steals(self) -> int:
        return self._team_stats.get('STL') if self._team_stats else None

    @property
    def blocks(self) -> int:
        return self._team_stats.get('BLK') if self._team_stats else None

    @property
    def turnovers(self) -> int:
        return self._team_stats.get('TO') if self._team_stats else None

    @property
    def personal_fouls(self) -> int:
        return self._team_stats.get('PF') if self._team_stats else None

    @property
    def points(self) -> int:
        return self._team_stats.get('PTS') if self._team_stats else None

    @property
    def plus_minus(self) -> float:
        return self._team_stats.get('PLUS_MINUS') if self._team_stats else None

    @property
    def score(self) -> str:
        return f"{self.points}:{self.opponent_points}"

    @staticmethod
    @retry(tries=RETRY_DELAY, delay=RETRY_ATTEMPTS)
    @functools.lru_cache(maxsize=1)
    def get_team_games(team_id: int, season: Season, date_from: datetime = None, date_to: datetime = None):
        if date_from:
            date_from = date_from.strftime('%m/%d/%Y')
        if date_to:
            date_to = date_to.strftime('%m/%d/%Y')
        game_finder = leaguegamefinder.LeagueGameFinder(season_nullable=season.name,
                                                        league_id_nullable='00',
                                                        team_id_nullable=team_id,
                                                        date_from_nullable=date_from,
                                                        date_to_nullable=date_to)
        return game_finder.get_normalized_dict().get('LeagueGameFinderResults')

    @property
    def team_player_ids(self) -> [int]:
        player_stats = self._traditional_stats.get('PlayerStats') if self._traditional_stats else None
        return [player.get('PLAYER_ID') for player in player_stats if player.get('TEAM_ID') == self.team_id]
