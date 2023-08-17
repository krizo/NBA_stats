import pytest

from nba_client.api_player import ApiPlayer


@pytest.fixture
def first_name():
    return "LeBron"


@pytest.fixture
def last_name():
    return "James"


def assert_player(player: ApiPlayer):
    assert player.first_name == 'LeBron'
    assert player.last_name == 'James'
    assert player.is_active
    assert player.player_id
    assert player.age
    assert player.weight
    assert player.height
    assert player.first_season_played == 2003
    assert player.draft_number == '1'
    assert player.draft_year == '2003'
    assert player.current_number
    assert player.country == "USA"
    assert player.school
    assert player.current_team_abbreviation == "LAL"
    assert player.player_id == 2544


def test_api_players(first_name, last_name):
    player = ApiPlayer(first_name, last_name)
    assert_player(player)


def test_api_players_by_id():
    player = ApiPlayer(id=2544)
    assert_player(player)
