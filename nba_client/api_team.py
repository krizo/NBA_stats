from nba_api.stats.static import teams

from helpers.helpers import find_in_collection
from nba_client.models.team_model import TeamModel


class ApiTeam:
    """ Class representing a team taken from NBA api client """

    _teams_cached = None

    def __init__(self, abbreviation: str):
        self._abbreviation = abbreviation

    @property
    def _team(self) -> TeamModel:
        team = self.get_team(self._abbreviation)
        if team is None:
            raise ValueError(
                f"Team can't be found by {self._abbreviation}. Call Teams.get_abbreviations() to get all valid values")
        return team

    @property
    def abbreviation(self) -> str:
        return self._team.abbreviation

    @property
    def id(self) -> int:
        return self._team.id

    @property
    def name(self) -> str:
        return self._team.name

    @property
    def nickname(self) -> str:
        return self._team.nickname

    @property
    def city(self) -> str:
        return self._team.city

    @property
    def state(self) -> str:
        return self._team.state

    @property
    def year_founded(self) -> int:
        return self._team.year_founded

    @classmethod
    def get_team(cls, abbreviation: str) -> TeamModel:
        team = find_in_collection(collection=cls.get_teams(), attribute='abbreviation', expected_value=abbreviation)
        if team:
            return TeamModel(id=team.get('id'), abbreviation=team.get('abbreviation'), name=team.get('full_name'),
                             nickname=team.get('nickname'), city=team.get('city'), state=team.get('state'),
                             year_founded=team.get('year_founded'))
        return None

    @classmethod
    def get_teams(cls) -> [dict]:
        if cls._teams_cached is None:
            cls._teams_cached = teams.get_teams()
        return cls._teams_cached

    @classmethod
    def get_abbreviations(cls) -> [str]:
        return [team.get('abbreviation') for team in cls.get_teams()]
