from datetime import datetime

from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams, players

from db.schema.db_team import Team
from db.schema.db_player import Player
from helpers.logger import Log
from nba_client.api_player import ApiPlayer
from nba_client.api_team import ApiTeam
from nba_client.season import Season


class Crawler:
    """ A bot which is getting through data provide by NBA stats api and persisitng them to local Database """

    @classmethod
    def persist_teams(cls):
        all_teams = teams.get_teams()
        Log.info(f"Persisting {len(all_teams)} teams.")
        for raw_team in teams.get_teams():
            api_team = ApiTeam(abbreviation=raw_team.get('abbreviation'))
            team = Team(id=api_team.id, name=api_team.name, short_name=api_team.abbreviation,
                        nickname=api_team.nickname,
                        state=api_team.state, city=api_team.city, year_founded=api_team.year_founded)
            Log.info(f"\tTeam: {team.name}")
            team.persist()
        Log.info("______________ Done ______________")

    @classmethod
    def persist_players(cls):
        all_players = players.get_players()
        Log.info(f"Persisting {len(all_players)} players.")
        ignored_players, persisted_players = [], 0
        for count, raw_player in enumerate(all_players):
            api_player = ApiPlayer(id=raw_player.get('id'))
            player = Player.create_from_api_model(api_player)
            team = Team.fetch_by_id(player.team_id)
            if team:
                Log.info(f"\tPlayer #{count + 1}: {api_player.first_name} {api_player.last_name} ({team.name})")
                player.persist()
                persisted_players += 1
            else:
                Log.warning(f"No Team found for {api_player.first_name} {api_player.last_name}")
                Log.warning("\tIgnoring.")
                ignored_players.append(f"{player.first_name} {player.last_name}")
        Log.info("______________ Done ______________")
        Log.info(f"Persisted players: {persisted_players}")
        Log.info(f"Ignored players count: {len(ignored_players)}")
        Log.info(f"\t{', '.join(ignored_players)}")

    @classmethod
    def persist_games(cls):
        team_id = 1610612738 # Boston
        number_of_seasons = 10
        current_year = datetime.now().year
        for n in range(0, number_of_seasons):
            # season_name = f"20{latest_season - (n + 1)}-{latest_season - n}"
            season = Season(start_year=current_year - (n + 1))
            gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable=season.name, league_id_nullable='00',
                                                           team_id_nullable=team_id)
            pass


# Database.recreate_database()
# Crawler.persist_teams()
# Crawler.persist_players()
