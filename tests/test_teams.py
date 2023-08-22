from typing import Any

import pytest

from db.database import Database
from db.schema.db_team import Team
from helpers.helpers import assert_equals, assert_model
from helpers.logger import Log
from nba_client.api_team import ApiTeam


@pytest.fixture
def team_id() -> int:
    return 1610612747


@pytest.fixture
def team_abbreviation() -> str:
    return "LAL"


@pytest.fixture
def expected_team(team_id, team_abbreviation) -> dict:
    return {
        "team_id": team_id,
        "city": 'Los Angeles',
        "abbreviation": team_abbreviation,
        "name": "Los Angeles Lakers",
        "nickname": "Lakers",
        "state": "California",
        "year_founded": 1948
    }


@pytest.fixture
def api_team(team_id, team_abbreviation) -> ApiTeam:
    return ApiTeam(team_abbreviation)


def setup():
    Database.recreate_database()


def test_api_client_teams(expected_team):
    assert len(ApiTeam.get_teams()) > 0
    team = ApiTeam('LAL')
    for attr, expected_value in expected_team.items():
        Log.info(f"Checking {attr} is {expected_value}")
        assert_equals(team.__getattribute__(attr), expected_value, attr)


def test_database_teams_create(api_team, expected_team):
    assert_model(model=Team.create_from_api_model(api_team), expected_values=expected_team)


def test_database_teams_fetch(api_team, expected_team):
    Team.create_from_api_model(api_team).persist()
    assert_model(model=Team.fetch_by_id(api_team.team_id), expected_values=expected_team)


def test_database_teams_update(api_team):
    updated_name = "Name updated"
    team = Team.fetch_by_id(api_team.team_id)
    api_team.name = updated_name
    team.update(updated_record=api_team, primary_key='team_id')
    team_updated = Team.fetch_by_id(api_team.team_id)
    assert_equals(team_updated.name, updated_name, "Updated name")
