import datetime

import pytest

from db.database import Database
from db.schema.db_game import Game
from db.schema.db_team import Team
from db.schema.db_team_game_stats import TeamGameStats
from helpers.helpers import assert_equals
from helpers.logger import Log
from nba_client.api_game import ApiGame
from nba_client.api_team import ApiTeam
from nba_client.api_team_game_stats import ApiTeamGameStats


@pytest.fixture
def team_id() -> id:
    return 1610612738


@pytest.fixture
def game_id() -> str:
    return '0042200307'


def setup():
    Database.recreate_database()
    Team.create_from_api_model(ApiTeam.get_team('MIA')).persist()
    Team.create_from_api_model(ApiTeam.get_team('BOS')).persist()
    api_game = ApiGame(game_id='0042200307')
    game = Game.create_from_api_model(api_model=api_game)
    game.persist()


@pytest.fixture
def api_tgs(game_id, team_id):
    return ApiTeamGameStats(game_id=game_id, team_id=team_id)


@pytest.fixture
def expected_stats(game_id, team_id):
    return {
        "game_id": game_id,
        "team_id": team_id,
        "team": "BOS",
        "opponent_team": "MIA",
        "game_date": datetime.datetime(2023, 5, 29, 0, 0),
        "home_team": "BOS",
        "home_team_id": team_id,
        "away_team_id": 1610612748,
        "away_team": "MIA",
        "result": "L",
        "points": 84,
        "opponent_points": 103,
        "score": "84:103",
        "played_at_home": True,
        "points_paint": 42,
        "points_2nd_chance": 13,
        "largest_lead": 5,
        "lead_changes": 1,
        "times_tied": 0,
        "minutes": 240,
        "fgm": 32,
        "fga": 82,
        "fg_pct": 0.39,
        "fg3m": 9,
        "fg3a": 42,
        "fg3_pct": 0.214,
        "ftm": 11,
        "fta": 13,
        "ft_pct": 0.846,
        "offensive_rebounds": 10,
        "defensive_rebounds": 30,
        "rebounds": 40,
        "assists": 18,
        "steals": 6,
        "blocks": 4,
        "turnovers": 15,
        "personal_fouls": 13,
        "plus_minus": -19.0,
        "points_off_to": 19
    }


def test_client_team_game_stats(api_tgs, game_id, team_id, expected_stats):
    for attr, expected_value in expected_stats.items():
        Log.info(f"Checking {attr}")
        assert_equals(api_tgs.__getattribute__(attr), expected_value, attr)


def test_database_team_game_stats_create(api_tgs, game_id, team_id, expected_stats):
    db_tgs = TeamGameStats.create_from_api_model(api_tgs)
    for attr, expected_value in expected_stats.items():
        Log.info(f"Checking {attr}")
        assert_equals(db_tgs.__getattribute__(attr), expected_value, attr)


def test_database_team_game_stats_fetch(api_tgs, expected_stats, team_id, game_id):
    TeamGameStats.create_from_api_model(api_tgs).persist()
    actual_record = TeamGameStats.fetch(team_id=team_id, game_id=game_id)
    for attr, expected_value in expected_stats.items():
        Log.info(f"Checking {attr}")
        assert_equals(actual_record.__getattribute__(attr), expected_value, attr)
