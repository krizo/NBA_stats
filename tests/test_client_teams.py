from nba_client.api_team import ApiTeam


def test_client_teams():
    assert len(ApiTeam.get_teams()) > 0
    lakers = ApiTeam.get_team('LAL')
    assert lakers
    assert lakers.name == "Los Angeles Lakers"
    assert lakers.abbreviation == 'LAL'
    assert lakers.nickname == 'Lakers'
    assert lakers.city == 'Los Angeles'
    assert lakers.state == 'California'
    assert lakers.year_founded == 1948
    assert lakers.id
    assert ApiTeam.get_team('LOL') is None

