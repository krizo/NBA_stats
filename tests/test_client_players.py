import pytest

from nba_client.player import Player


@pytest.fixture
def first_name():
    return "Lebron"


@pytest.fixture
def last_name():
    return "James"


def test_client_players(first_name, last_name):
    player = Player(first_name, last_name)
    assert player.first_name == first_name
    assert player.last_name == last_name
    assert player.is_active
    assert player.player_id
    assert player.age
    assert player.weight
    assert player.height
    assert player.first_season_played == 2003
    assert player.draft_number == 1
    assert player.draft_year == 2003
    assert player.current_number
    assert player.country == "USA"
    assert player.school
    assert player.current_team_abbreviation == "LAL"
