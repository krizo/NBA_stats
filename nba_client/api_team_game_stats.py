from datetime import datetime

from nba_api.stats.endpoints import leaguegamefinder, BoxScoreSummaryV2, BoxScoreTraditionalV2

from db.schema.db_team import Team
from nba_client.season import Season


class ApiTeamGameStats:
    """ Class representing a game stats for specific team taken from NBA api client """

    def __init__(self, game_id: str, team_id: int):
        self.game_id = game_id
        self.team_id = team_id
        self._inf = None
        self._stats = None

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
    def _other_stats(self) -> dict or None:
        if self._box_score_summary:
            return self._get_team_stats(self._box_score_summary.get('OtherStats'))
        return None

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
            return self._get_team_stats(self._traditional_stats.get('TeamStats'))
        return None

    @property
    def _opponent_team_stats(self) -> dict or None:
        if self._traditional_stats:
            return self._get_team_stats(self._traditional_stats.get('TeamStats'), self.opponent_team_id)
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
    def played_at_home(self) -> bool:
        return self.home_team_id == self.team_id

    @property
    def away_team_id(self) -> int:
        return self._summary.get('VISITOR_TEAM_ID') if self._summary else None

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
    def points_paint(self) -> int:
        return self._other_stats.get('PTS_PAINT') if self._other_stats else None

    @property
    def points_2nd_chance(self) -> int:
        return self._other_stats.get('PTS_2ND_CHANCE') if self._other_stats else None

    @property
    def largest_lead(self) -> int:
        return self._other_stats.get('LARGEST_LEAD') if self._other_stats else None

    @property
    def lead_changes(self) -> int:
        return self._other_stats.get('LEAD_CHANGES') if self._other_stats else None

    @property
    def times_tied(self) -> int:
        return self._other_stats.get('TIMES_TIED') if self._other_stats else None

    @property
    def points_off_to(self) -> int:
        """ The number of points scored by a player or team following an opponent's turnover """
        return self._other_stats.get('PTS_OFF_TO') if self._other_stats else None

    @property
    def minutes(self) -> str:
        return self._team_stats.get('MIN') if self._team_stats else None

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
        return self._team_stats.get('reb') if self._team_stats else None

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
    def opponent_points(self) -> int:
        return self._opponent_team_stats.get('PTS') if self._opponent_team_stats else None

    @property
    def plus_minus(self) -> float:
        return self._team_stats.get('PLUS_MINUS') if self._team_stats else None

    @property
    def result(self):
        return 'W' if self.points > self.opponent_points else 'L'

    @property
    def score(self) -> str:
        return f"{self.points}:{self.opponent_points}"

    def _get_team_stats(self, stats: list[dict], team_id: int = None) -> dict or None:
        team_id = team_id or self.team_id
        try:
            return next(s for s in stats if s['TEAM_ID'] == team_id)
        except StopIteration:
            return None

    @staticmethod
    def get_team_games(team_id: int, season: Season):
        gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season.name, league_id_nullable='00',
                                                       team_id_nullable=team_id)
        return gamefinder.get_normalized_dict().get('LeagueGameFinderResults')
