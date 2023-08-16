from nba_client.team import Team


def test_client_teams():
    assert len(Team.get_teams()) > 0
    lakers = Team.get_team('LAL')
    assert lakers
    assert lakers.name == "Los Angeles Lakers"
    assert lakers.abbreviation == 'LAL'
    assert lakers.nickname == 'Lakers'
    assert lakers.city == 'Los Angeles'
    assert lakers.state == 'California'
    assert lakers.year_founded == 1948
    assert lakers.id
    assert Team.get_team('LOL') is None

