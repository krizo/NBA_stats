from nba_api.stats.static import teams

from helpers.helpers import find_in_collection
from nba_client.models.team_model import TeamModel


class ApiTeam:
    """ Class representing a team taken from NBA api client """

    _teams_cached = None

    def __init__(self, abbreviation: str):
        self.abbreviation = abbreviation
        self._team_props = None
        self.team_id: int = self._team_properties.get('id')
        self.name: str = self._team_properties.get('full_name')
        self.nickname: str = self._team_properties.get('nickname')
        self.city: str = self._team_properties.get('city')
        self.state: str = self._team_properties.get('state')
        year_founded = self._team_properties.get('year_founded')
        self.year_founded: int = int(year_founded) if year_founded else None

    @property
    def _team_properties(self) -> dict:
        if self._team_props is None:
            self._team_props = self._team.items()
        return dict(self._team_props)

    @property
    def _team(self) -> dict:
        team = self._get_team(self.abbreviation)
        if team is None:
            raise ValueError(
                f"Team can't be found by {self.abbreviation}. Call Teams.get_abbreviations() to get all valid values")
        return team

    @classmethod
    def _get_team(cls, abbreviation: str) -> TeamModel or None:
        return find_in_collection(collection=cls.get_teams(), attribute='abbreviation', expected_value=abbreviation)

    @classmethod
    def get_teams(cls) -> [dict]:
        if cls._teams_cached is None:
            cls._teams_cached = teams.get_teams()
        return cls._teams_cached

    @classmethod
    def get_abbreviations(cls) -> [str]:
        return [team.get('abbreviation') for team in cls.get_teams()]
