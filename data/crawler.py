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
    def get_full_data_for_season(cls, season: Season, test_mode: bool = False, ignored_teams: [str] = None):
        players_persisted, games_persisted, players_stats_persisted, teams_stats_persisted = 0, 0, 0, 0
        games_ignored = []
        ignored_teams = ignored_teams or []
        for team in Team.fetch_all():
            if team.abbreviation in ignored_teams or None:
                continue
            Log.info(f"\tTeam: {team.name}")
            season_games = ApiTeamGameStats.get_team_games(team_id=team.team_id, season=season)
            season_games = season_games if test_mode else season_games
            Log.info(f"\t{team.name} played {len(season_games)} games in season {season.name}")
            for index, team_game in enumerate(season_games):
                api_game = ApiGame(game_id=team_game.get('GAME_ID'))
                try:
                    game = Game.create_from_api_model(api_game)
                except (AttributeError, ValueError) as ex:
                    Log.error(ex)
                    games_ignored.append(api_game.game_id)
                    continue
                Log.info(f"\t\tGame #{index + 1}: {api_game.game_id} - {game.matchup}")
                if not Game.fetch_by_id(game_id=api_game.game_id):
                    game.persist()
                    games_persisted += 1
                api_game_stats = ApiTeamGameStats(game_id=api_game.game_id, team_id=team.team_id)
                tgs = TeamGameStats.create_from_api_model(api_game_stats)
                tgs.persist()
                teams_stats_persisted += 1
                for player_id in api_game_stats.team_player_ids:
                    try:
                        api_player = ApiPlayer(player_id=player_id)
                    except ValueError:
                        Log.warning(f"Player {player_id} cant' be found. Ignoring")
                        continue
                    Log.info(f"\t\t\tPlayer: {api_player.full_name}")
                    player = Player.create_from_api_model(api_player)
                    if not Player.fetch_by_id(player_id):
                        player.persist()
                        players_persisted += 1
                    api_pst = ApiPlayerGameStats(game_id=api_game.game_id, player_id=player_id)
                    pgs = PlayerGameStats.create_from_api_model(api_pst)
                    if not PlayerGameStats.fetch(player_id=player_id, game_id=api_game.game_id):
                        pgs.persist()
                        players_stats_persisted += 1
                Log.info(f"\t\t----- Game {api_game.game_id} done -----")
            Log.info(f"\t----- Team {team.name} done -----")
        Log.info(f"----- Season {season.name} done -----")
        Log.info(f"Players added: {players_persisted}")
        Log.info(f"Games added: {games_persisted}")
        Log.info(f"Games ignored ({len(games_ignored)}: {', '.join(games_ignored)}")
        Log.info(f"Team stats added: {teams_stats_persisted}")
        Log.info(f"Player stats added: {players_stats_persisted}")


Database.recreate_database()
Crawler.persist_teams()
# ignore_teams = ['ATL', 'BOS', 'CLE', 'NOP', 'CHI', 'DAL', 'DEN', 'GSW', 'HOU']
ignore_teams = None
Crawler.get_full_data_for_season(season=Season(start_year=2022), test_mode=True, ignored_teams=ignore_teams)
