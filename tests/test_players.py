import datetime

import pytest

from db.database import Database
from db.schema.db_player import Player
from db.schema.db_team import Team
from helpers.helpers import assert_equals, assert_model
from nba_client.api_player import ApiPlayer
from nba_client.api_team import ApiTeam


@pytest.fixture
def first_name() -> str:
    return "LeBron"


@pytest.fixture
def last_name() -> str:
    return "James"


@pytest.fixture
def player_id() -> int:
    return 2544


@pytest.fixture
def api_player() -> ApiPlayer:
    return ApiPlayer(first_name="LeBron", last_name="James")


def setup():
    Database.recreate_database()
    Team.create_from_api_model(ApiTeam('LAL')).persist()


@pytest.fixture
def expected_player(first_name, last_name, player_id):
    return {
        "first_name": first_name,
        "last_name": last_name,
        "is_active": True,
        "player_id": 2544,
        "age": datetime.datetime.now().year - 1985,
        "weight": 113,
        "height": 206,
        "first_season_played": 2003,
        "draft_number": '1',
        "draft_year": '2003',
        "current_number": 23,
        "country": "USA",
        "school": 'St. Vincent-St. Mary HS (OH)',
        "current_team_abbreviation": "LAL",
    }


def test_api_players_by_name(first_name, last_name, expected_player):
    assert_model(model=ApiPlayer(first_name, last_name), expected_values=expected_player)


def test_api_players_by_id(player_id, expected_player):
    assert_model(model=ApiPlayer(player_id=player_id), expected_values=expected_player)


def test_database_player_create(api_player, expected_player):
    player = Player.create_from_api_model(api_model=api_player)
    assert_model(model=player, expected_values=expected_player)


def test_database_players_fetch(api_player, expected_player):
    Player.create_from_api_model(api_model=api_player).persist()
    assert_model(model=Player.fetch_by_id(api_player.player_id), expected_values=expected_player)


def test_database_players_update(api_player):
    updated_name = "Name updated"
    player = Player.fetch_by_id(api_player.player_id)
    api_player.last_name = updated_name
    player.update(api_player, primary_key='player_id')
    player_updated = Player.fetch_by_id(api_player.player_id)
    assert_equals(player_updated.last_name, updated_name, "Updated name")
