import pytest

from db.database import Database
from db.schema.db_team import Team
from db.schema.db_player import Player
from helpers.helpers import assert_equals
from nba_client.api_player import ApiPlayer
from nba_client.api_team import ApiTeam
from nba_client.models.player_model import PlayerModel


@pytest.fixture
def api_player() -> PlayerModel:
    api_player = ApiPlayer(first_name="Lebron", last_name="James")
    return api_player.get_player()


def setup():
    Database.recreate_database()
    Team.create_from_api_model(ApiTeam.get_team('LAL')).persist()


def test_database_player_create(api_player):
    player = Player.create_from_api_model(api_model=api_player)
    player.persist()


def test_database_players_fetch(api_player):
    actual_player = Player.fetch_by_id(api_player.id)
    assert actual_player


def test_database_players_update(api_player):
    updated_name = "Name updated"
    player = Player.fetch_by_id(api_player.id)
    api_player.last_name = updated_name
    player.update(api_player)

    player_updated = Player.fetch_by_id(api_player.id)
    assert_equals(player_updated.last_name, updated_name, "Updated name")
