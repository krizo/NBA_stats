import pytest

from db.database import Database
from db.schema.db_team import Team
from db.schema.db_team_game_stats import TeamGameStats
from helpers.helpers import assert_equals
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


@pytest.fixture
def api_gst(game_id, team_id):
    return ApiTeamGameStats(game_id=game_id, team_id=team_id)


def test_client_team_game_stats_create(api_gst, game_id, team_id):
    tg = TeamGameStats.create_from_api_model(api_gst)
    assert tg
    assert_equals(tg.game_id, game_id, "Game id")
    assert_equals(tg.team_id, team_id, "Team id")
    assert_equals(tg.team, api_gst.team, "Team")
    assert_equals(tg.home_team, api_gst.home_team, "Home Team")
    assert_equals(tg.home_team_id, api_gst.home_team_id, "Home Team Id")
    assert_equals(tg.away_team, api_gst.away_team, "Away Team")
    assert_equals(tg.away_team_id, api_gst.away_team_id, "Away Team Id")
    assert_equals(tg.plus_minus, api_gst.plus_minus, 'plus minus')
    assert_equals(tg.personal_fouls, api_gst.personal_fouls, "Personal Fouls")
    assert_equals(tg.score, api_gst.score, "Score")
    assert_equals(tg.result, api_gst.result, "Result")
    assert_equals(tg.turnovers, api_gst.turnovers, "Turnovers")
    assert_equals(tg.blocks, api_gst.blocks, "Blocks")
    assert_equals(tg.steals, api_gst.steals, "Steals")
    assert_equals(tg.assists, api_gst.assists, "Assists")
    assert_equals(tg.rebounds, api_gst.rebounds, "Rebounds")
    assert_equals(tg.defensive_rebounds, api_gst.defensive_rebounds, "Defensive Rebounds")
    assert_equals(tg.offensive_rebounds, api_gst.offensive_rebounds, "Offensive Rebounds")
    assert_equals(tg.ft_pct, api_gst.ft_pct, "Ft_pct")
    assert_equals(tg.ftm, api_gst.ftm, "Ftm")
    assert_equals(tg.fta, api_gst.fta, "Fta")
    assert_equals(tg.fg_pct, api_gst.fg_pct, "Fg_pct")
    assert_equals(tg.fgm, api_gst.fgm, "Fgm")
    assert_equals(tg.fga, api_gst.fga, "Fga")
    assert_equals(tg.fg3_pct, api_gst.fg3_pct, "Fg_pct")
    assert_equals(tg.fg3m, api_gst.fg3m, "Fg3m")
    assert_equals(tg.fg3a, api_gst.fg3a, "Fg3a")
    assert_equals(tg.minutes, api_gst.minutes, "Minutes")
    assert_equals(tg.times_tied, api_gst.times_tied, "Times tied")
    assert_equals(tg.lead_changes, api_gst.lead_changes, "Lead changes")
    assert_equals(tg.largest_lead, api_gst.largest_lead, "Largest Lead")
    assert_equals(tg.points_2nd_chance, api_gst.points_2nd_chance, "Points 2nd chance")
    assert_equals(tg.points_paint, api_gst.points_paint, "Points paint")
    assert_equals(tg.points_off_to, api_gst.points_off_to, "Points off to")
    assert_equals(tg.played_at_home, api_gst.played_at_home, "Played at home")
