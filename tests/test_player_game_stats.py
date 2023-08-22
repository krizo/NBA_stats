import datetime

import pytest

from db.database import Database
from db.schema.db_game import Game
from db.schema.db_player import Player
from db.schema.db_player_game_stats import PlayerGameStats
from db.schema.db_team import Team
from helpers.helpers import assert_equals
from helpers.logger import Log
from nba_client.api_game import ApiGame
from nba_client.api_player import ApiPlayer
from nba_client.api_player_game_stats import ApiPlayerGameStats
from nba_client.api_team import ApiTeam


@pytest.fixture
def player_id() -> id:
    player_id = 1628369
    api_player = ApiPlayer(player_id=player_id)
    Player.create_from_api_model(api_player).persist()
    return player_id


@pytest.fixture
def game_id() -> str:
    game_id = '0042200307'
    api_game = ApiGame(game_id)
    Game.create_from_api_model(api_game).persist()
    return game_id


@pytest.fixture
def api_pst(game_id, player_id):
    return ApiPlayerGameStats(game_id=game_id, player_id=player_id)


def setup():
    Database.recreate_database()
    Team.create_from_api_model(ApiTeam('MIA')).persist()
    Team.create_from_api_model(ApiTeam('BOS')).persist()
    api_game = ApiGame(game_id='0042200307')
    game = Game.create_from_api_model(api_model=api_game)
    game.persist()


@pytest.fixture
def expected_stats(game_id, player_id):
    return {
        "game_id": game_id,
        "team_id": 1610612738,
        "player_id": player_id,
        "home_team_id": 1610612738,
        "away_team_id": 1610612748,
        "opponent_team_id": 1610612748,
        "team": "BOS",
        "opponent_team": "MIA",
        "game_date": datetime.datetime(2023, 5, 29, 0, 0),
        "season": "2022-23",
        "team_points": 84,
        "opponent_points": 103,
        "player_name": "Jayson Tatum",
        "minutes": 41,
        "fgm": 5,
        "fga": 13,
        "fg_pct": 0.385,
        "fg3m": 1,
        "fg3a": 4,
        "fg3_pct": 0.25,
        "ftm": 3,
        "fta": 4,
        "ft_pct": 0.75,
        "offensive_rebounds": 2,
        "defensive_rebounds": 9,
        "rebounds": 11,
        "assists": 4,
        "steals": 1,
        "blocks": 0,
        "turnovers": 2,
        "personal_fouls": 2,
        "points": 14,
        "plus_minus": -12,
        "played_at_home": True,
        "score": "84:103",
        "result": "L",
    }


def test_client_player_game_stats(api_pst, expected_stats, player_id, game_id):
    for attr, expected_value in expected_stats.items():
        Log.info(f"Checking {attr} is {expected_value}")
        assert_equals(api_pst.__getattribute__(attr), expected_value, attr)


def test_database_player_game_stats_create(api_pst, expected_stats, player_id, game_id):
    db_pst = PlayerGameStats.create_from_api_model(api_pst)
    for attr, expected_value in expected_stats.items():
        Log.info(f"Checking {attr} is {expected_value}")
        assert_equals(db_pst.__getattribute__(attr), expected_value, attr)


def test_database_player_game_stats_fetch(api_pst, expected_stats, player_id, game_id):
    PlayerGameStats.create_from_api_model(api_pst).persist()
    actual_record = PlayerGameStats.fetch(player_id=player_id, game_id=game_id)
    for attr, expected_value in expected_stats.items():
        Log.info(f"Checking {attr} is {expected_value}")
        assert_equals(actual_record.__getattribute__(attr), expected_value, attr)
