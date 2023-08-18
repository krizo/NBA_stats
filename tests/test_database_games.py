import pytest

from db.database import Database
from db.db_game import Game
from db.db_team import Team
from nba_client.api_game import ApiGame
from nba_client.api_team import ApiTeam


@pytest.fixture
def api_game() -> ApiGame:
    return ApiGame(game_id='0042200307')


def setup():
    Database.drop_table(Game)
    Database.create_table(Game)
    Team.create_from_api_model(ApiTeam.get_team('BOS')).persist()
    Team.create_from_api_model(ApiTeam.get_team('MIA')).persist()


def test_database_game_create(api_game):
    game = Game.create_from_api_model(api_model=api_game)
    game.persist()


def test_database_game_fetch(api_game):
    actual_game = Game.fetch_by_id(api_game.game_id)
    assert actual_game
