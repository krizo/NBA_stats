import pytest

from db.database import Database
from db.db_game import Game
from nba_client.api_game import ApiGame


@pytest.fixture
def api_game() -> ApiGame:
    return ApiGame(game_id='0042200307')


def setup():
    Database.drop_table(Game)
    Database.create_table(Game)


def test_database_game_create(api_game):
    game = Game.create_from_api_model(api_model=api_game)
    game.persist()


def test_database_game_fetch(api_game):
    actual_game = Game.fetch_by_id(api_game.game_id)
    assert actual_game
