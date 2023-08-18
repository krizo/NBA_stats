import pytest

from helpers.helpers import assert_equals
from nba_client.api_game import ApiGame


@pytest.fixture
def game_id() -> str:
    return '0042200307'


@pytest.fixture
def home_team_id() -> int:
    return 1610612738


@pytest.fixture
def away_team_id() -> int:
    return 1610612748


@pytest.fixture
def game(game_id) -> ApiGame:
    return ApiGame(game_id=game_id)


def test_api_client_games(game, game_id, away_team_id, home_team_id):
    assert_equals(game.game_id, game_id, 'Game id')
    assert game
    assert_equals(game.away_team_id, away_team_id, 'away_team_id')
    assert_equals(game.home_team_id, home_team_id, 'home_team_id')
    assert game.away_team == 'MIA'
    assert game.home_team == 'BOS'
    assert game.away_team_points > 0
    assert game.home_team_points > 0
    assert game.attendance > 0
    assert game.matchup
    assert game.score
    assert game.status
    assert game.winner
    assert game.game_date
