import datetime

from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.static import players
from retry import retry

from helpers.helpers import lists_to_dict, convert_to_metric


class ApiPlayer:
    """ Class representing a player taken from NBA api client """

    def __init__(self, first_name: str = None, last_name: str = None, player_id: int = None):
        self.first_name = first_name
        self.last_name = last_name
        self._player_data: dict = None
        if self.first_name and self.last_name:
            self._player_data = self._get_player_by_name(self.first_name, self.last_name)
        elif player_id:
            self._player_data = self._get_player_by_id(player_id)
            if self._player_data:
                self.first_name = self._player_data.get("first_name")
                self.last_name = self._player_data.get("last_name")
        else:
            raise ValueError("Provide either first_name and last_name or player id")
        if not self._player_data:
            raise ValueError("Player data can't be found")
        self.player_id: int = self._player_data.get('id')
        self.is_active: bool = self._player_data.get('is_active')
        weight, height = self._player_data.get('weight'), self._player_data.get('height')
        self.weight: int = int(weight) if weight else None
        self.height: int = int(height) if height else None
        self.draft_number: str = str(self._player_data.get('draft_number'))
        self.draft_year: str = str(self._player_data.get('draft_year'))
        team_id = self._player_data.get('current_team_id')
        self.current_team_id: int = None if team_id == 0 else team_id
        current_number = self._player_data.get('current_number')
        self.current_number: int = int(current_number) if current_number else None
        self.first_season_played: int = self._player_data.get('first_season_played')
        self.country: str = self._player_data.get('country')
        self.birth_date: datetime.date = self._player_data.get('birth_date')
        self.age: int = int((datetime.datetime.now() - self.birth_date).days / 365.25)
        self.school: str = self._player_data.get('school')
        self.current_team_abbreviation = self._player_data.get('current_team_abbreviation')
        self.full_name = self._player_data.get('full_name')
        self.position = self._player_data.get('position')

    @staticmethod
    def _get_player_by_name(first_name: str, last_name: str) -> dict:
        @retry(tries=10, delay=10)
        def get_players():
            return players.find_players_by_full_name(f'{first_name} {last_name}')

        players_found = get_players(first_name, last_name)
        assert players_found, f"No player found: {first_name} {last_name}"
        assert len(players_found) == 1, \
            f"More players found for {first_name} {last_name}: {', '.join([p['full_name'] for p in players_found])}"
        player_data = players_found[0]
        return ApiPlayer._get_additional_stats(player_data)

    @staticmethod
    def _get_player_by_id(player_id: int) -> dict or None:
        player_found = players.find_player_by_id(player_id=player_id)
        if not player_found:
            return None
        return ApiPlayer._get_additional_stats(player_found)

    @staticmethod
    def _get_additional_stats(player_data):
        @retry(tries=10, delay=10)
        def _get_common_data(player_id: int):
            return commonplayerinfo.CommonPlayerInfo(player_id=player_id).common_player_info.get_dict()

        common_data =_get_common_data(player_data['id'])
        additional_data = lists_to_dict(common_data.get('headers'), common_data.get('data')[0])
        height = additional_data['HEIGHT']
        weight = additional_data['WEIGHT']
        player_data['school'] = additional_data['SCHOOL']
        player_data['birth_date'] = datetime.datetime.strptime(additional_data['BIRTHDATE'].split('T')[0], "%Y-%m-%d")
        player_data['country'] = additional_data['COUNTRY']
        player_data['position'] = additional_data['POSITION']
        player_data['current_team_abbreviation'] = additional_data['TEAM_ABBREVIATION']
        player_data['current_team_id'] = int(additional_data['TEAM_ID'])
        player_data['current_number'] = additional_data['JERSEY']
        player_data['position'] = additional_data['POSITION']
        player_data['draft_year'] = additional_data['DRAFT_YEAR']
        player_data['draft_number'] = additional_data['DRAFT_NUMBER']
        if height:
            height_feet, height_inches = additional_data['HEIGHT'].split('-')
            player_data['height'] = convert_to_metric(feet=int(height_feet), inches=int(height_inches))
        else:
            player_data['height'] = None
        if weight:
            player_data['weight'] = int(int(additional_data['WEIGHT']) // 2.205)
        else:
            player_data['weight'] = None
        player_data['first_season_played'] = int(additional_data['FROM_YEAR'])
        return player_data
