import pytest

from db.database import Database
from db.db_schema import Team
from helpers.helpers import assert_equals
from nba_client.api_team import ApiTeam
from nba_client.models.team_model import TeamModel


@pytest.fixture
def api_team() -> TeamModel:
    return ApiTeam.get_team('LAL')


def setup():
    Database.recreate_database()


def assert_team(actual: Team, expected: TeamModel):
    assert_equals(actual.id, expected.id, 'Team id')
    assert_equals(actual.name, expected.name, 'Team name')
    assert_equals(actual.city, expected.city, 'Team city')
    assert_equals(actual.state, expected.state, 'Team state')
    assert_equals(actual.nickname, expected.nickname, 'Team nickname')
    assert_equals(actual.short_name, expected.abbreviation, 'Team short name')
    assert_equals(actual.year_founded, expected.year_founded, 'Team year founded')
    assert actual.created_at
    assert actual.updated_at


def test_database_teams_create(api_team):
    team = Team.create_from_api_model(api_team)
    team.persist()


def test_database_teams_fetch(api_team):
    actual_team = Team.fetch_by_id(api_team.id)
    assert_team(actual_team, api_team)


def test_database_teams_update(api_team):
    updated_name = "Name updated"
    team = Team.fetch_by_id(api_team.id)
    api_team.name = updated_name
    team.update(api_team)

    team_updated = Team.fetch_by_id(api_team.id)
    assert_equals(team_updated.name, updated_name, "Updated name")
