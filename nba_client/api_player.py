import datetime

from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players

from helpers.helpers import lists_to_dict, convert_to_metric
from nba_client.models.player_model import PlayerModel


class ApiPlayer:
    """ Class representing a player taken from NBA api client """

    _data = None

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def _info(self) -> PlayerModel:
        if self._data is None:
            self._data = self._get_player_by_name(self.first_name, self.last_name)
        return self._data

    @property
    def is_active(self) -> bool:
        return self._info.is_active

    @property
    def full_name(self) -> str:
        return self._info.full_name

    @property
    def player_id(self) -> int:
        return self._info.id

    @property
    def school(self) -> str:
        return self._info.school

    @property
    def birth_date(self) -> datetime:
        return self._info.birth_date

    @property
    def country(self) -> str:
        return self._info.country

    @property
    def position(self) -> str:
        return self._info.position

    @property
    def current_team_abbreviation(self) -> str:
        return self._info.current_team_abbreviation

    @property
    def current_number(self) -> int:
        return self._info.current_number

    @property
    def height(self) -> int:
        return self._info.height

    @property
    def weight(self) -> int:
        return self._info.weight

    @property
    def first_season_played(self) -> int:
        return self._info.first_season_played

    @property
    def age(self) -> int:
        return self._info.age

    @property
    def draft_year(self) -> int:
        return self._info.draft_year

    @property
    def draft_number(self) -> int:
        return self._info.draft_number

    @staticmethod
    def _get_player_by_name(first_name: str, last_name: str) -> PlayerModel:
        players_found = players.find_players_by_full_name(f'{first_name} {last_name}')
        assert players_found, f"No player found: {first_name} {last_name}"
        assert len(
            players_found) == 1, f"More players found for {first_name} {last_name}: {', '.join([p['full_name'] for p in players_found])}"
        player_data = players_found[0]
        common_data = commonplayerinfo.CommonPlayerInfo(player_id=player_data['id']).common_player_info.get_dict()
        additional_data = lists_to_dict(common_data.get('headers'), common_data.get('data')[0])
        player_data['school'] = additional_data['SCHOOL']
        player_data['birth_date'] = datetime.datetime.strptime(additional_data['BIRTHDATE'].split('T')[0], "%Y-%m-%d")
        player_data['country'] = additional_data['COUNTRY']
        player_data['position'] = additional_data['POSITION']
        player_data['current_team_abbreviation'] = additional_data['TEAM_ABBREVIATION']
        player_data['current_number'] = int(additional_data['JERSEY'])
        player_data['position'] = additional_data['POSITION']
        player_data['draft_year'] = int(additional_data['DRAFT_YEAR'])
        player_data['draft_number'] = int(additional_data['DRAFT_NUMBER'])
        height_feet, height_inches = additional_data['HEIGHT'].split('-')
        player_data['height'] = convert_to_metric(feet=int(height_feet), inches=int(height_inches))
        player_data['weight'] = int(int(additional_data['WEIGHT']) // 2.205)
        player_data['first_season_played'] = int(additional_data['FROM_YEAR'])
        return PlayerModel(**player_data)
