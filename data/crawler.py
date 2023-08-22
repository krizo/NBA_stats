from nba_api.stats.static import teams, players

from db.database import Database
from db.schema.db_game import Game
from db.schema.db_player_game_stats import PlayerGameStats
from db.schema.db_team import Team
from db.schema.db_player import Player
from db.schema.db_team_game_stats import TeamGameStats
from helpers.logger import Log
from nba_client.api_game import ApiGame
from nba_client.api_player import ApiPlayer
from nba_client.api_player_game_stats import ApiPlayerGameStats
from nba_client.api_team import ApiTeam
from nba_client.api_team_game_stats import ApiTeamGameStats
from nba_client.season import Season


class Crawler:
    """ A bot which is getting through data provide by NBA stats api and persisitng them to local Database """

    @classmethod
    def persist_teams(cls) -> [Team]:
        all_teams = teams.get_teams()
        Log.info(f"Persisting {len(all_teams)} teams.")
        persisited_teams = []
        for raw_team in all_teams:
            api_team = ApiTeam(abbreviation=raw_team.get('abbreviation'))
            team = Team.create_from_api_model(api_team)
            Log.info(f"\tTeam: {team.name}")
            team.persist()
            persisited_teams.append(team)
        Log.info("______________ Teams Done ______________")
        return persisited_teams

    @classmethod
    def persist_players(cls, test_mode: bool = False):
        all_players = players.get_players()
        if test_mode:
            all_players = all_players[9]
        Log.info(f"Persisting {len(all_players)} players.")
        ignored_players, persisted_players = [], 0
        for count, raw_player in enumerate(all_players):
            api_player = ApiPlayer(player_id=raw_player.get('id'))
            player = Player.create_from_api_model(api_player)
            team = Team.fetch_by_id(player.player_id)
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
    def get_full_data_for_season(cls, season: Season, test_mode: bool = False):
        for team in Team.fetch_all():
            Log.info(f"\tTeam: {team.name}")
            season_games = ApiTeamGameStats.get_team_games(team_id=team.team_id, season=season)
            season_games = season_games if test_mode else season_games
            Log.info(f"\t{team.name} played {len(season_games)} games in season {season.name}")
            for index, team_game in enumerate(season_games):
                api_game = ApiGame(game_id=team_game.get('GAME_ID'))
                game = Game.create_from_api_model(api_game)
                Log.info(f"\t\tGame #{index + 1}: {api_game.game_id} - {game.matchup}")
                if not Game.fetch_by_id(game_id=api_game.game_id):
                    game.persist()
                api_game_stats = ApiTeamGameStats(game_id=api_game.game_id, team_id=team.team_id)
                tgs = TeamGameStats.create_from_api_model(api_game_stats)
                tgs.persist()
                for player_id in api_game_stats.team_player_ids:
                    api_player = ApiPlayer(player_id=player_id)
                    Log.info(f"\t\t\tPlayer: {api_player.full_name}")
                    player = Player.create_from_api_model(api_player)
                    if not Player.fetch_by_id(player_id):
                        player.persist()
                    api_pst = ApiPlayerGameStats(game_id=api_game.game_id, player_id=player_id)
                    pgs = PlayerGameStats.create_from_api_model(api_pst)
                    if not PlayerGameStats.fetch(player_id=player_id, game_id=api_game.game_id):
                        pgs.persist()
                Log.info(f"\t\t----- Game {api_game.game_id} done -----")
            Log.info(f"\t----- Team {team.name} done -----")
        Log.info(f"----- Season {season.name} done -----")


Database.recreate_database()
Crawler.persist_teams()
Crawler.get_full_data_for_season(season=Season(start_year=2022), test_mode=True)