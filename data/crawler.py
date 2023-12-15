import datetime

from nba_api.stats.static import teams

from db.database import Database
from db.schema.db_game import Game
from db.schema.db_play_by_play import PlayByPlay
from db.schema.db_player_game_stats import PlayerGameStats
from db.schema.db_player_shots import PlayerShots
from db.schema.db_team import Team
from db.schema.db_player import Player
from db.schema.db_team_game_stats import TeamGameStats
from helpers.logger import Log
from nba_client.api_game import ApiGame
from nba_client.api_play_by_play import ApiPlayByPlay
from nba_client.api_player import ApiPlayer
from nba_client.api_player_game_shots import ApiPlayerSeasonShots
from nba_client.api_player_game_stats import ApiPlayerGameStats
from nba_client.api_team import ApiTeam
from nba_client.api_team_game_stats import ApiTeamGameStats
from nba_client.season import Season
from nba_client.season_type import SeasonType


class Crawler:
    """ A bot which is getting through data provide by NBA stats api and persisting them to local Database """

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
    def get_data_for_season(cls, season: Season, test_mode: bool = False, ignored_teams: [str] = None,
                            date_from: datetime = None,
                            date_to: datetime = None):
        start_time = datetime.datetime.now()
        players_persisted, games_persisted, players_stats_persisted, teams_stats_persisted = 0, 0, 0, 0
        games_ignored = []
        ignored_teams = ignored_teams or []
        for team_index, team in enumerate(Team.fetch_all()):
            if team.abbreviation in ignored_teams or None:
                continue

            Log.info(f"\t#{team_index + 1} Team: {team.name} ({season})")
            season_games = ApiTeamGameStats.get_team_games(team_id=team.team_id, season=season, date_from=date_from,
                                                           date_to=date_to)
            season_games = season_games if test_mode else season_games
            if date_to and date_from:
                Log.info(
                    f"\t{team.name} played {len(season_games)} games in "
                    f"timefrme {date_from.strftime('%m/%d/%Y')} - {date_to.strftime('%m/%d/%Y')}")
            else:
                Log.info(f"\t{team.name} played {len(season_games)} games in season {season.name}")
            for index, team_game in enumerate(season_games):
                api_game = ApiGame(game_id=team_game.get('GAME_ID'))
                try:
                    game = Game.create_from_api_model(api_game)
                except (AttributeError, ValueError) as ex:
                    Log.error(ex)
                    games_ignored.append(api_game.game_id)
                    continue
                Log.info(
                    f"\t\tGame #{index + 1}: {api_game.game_id} - {game.matchup} ({game.game_date.strftime('%d-%m-%Y')})")
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
        end_time = datetime.datetime.now()
        Log.info(f"----- Season {season.name} done -----")
        Log.info(f"Start time: {start_time}")
        Log.info(f"End time: {end_time}")
        Log.info(f"Players added: {players_persisted}")
        Log.info(f"Games added: {games_persisted}")
        Log.info(f"Games ignored ({len(games_ignored)}: {', '.join(games_ignored)}")
        Log.info(f"Team stats added: {teams_stats_persisted}")
        Log.info(f"Player stats added: {players_stats_persisted}")

    @classmethod
    def get_play_by_play_data_for_season(cls, season: Season, ignore_season_types: [] = None):
        start_time = datetime.datetime.now()
        Log.info(f"Getting Play by Play data for all games in season {season}")
        season_games = ApiGame.get_games(season=season)
        Log.info(f"{int(len(season_games) / 2)} games found in season {season}.")
        records_added = 0
        game_ids_done, games_ignored = [], []

        for game_counter, api_game in enumerate(season_games):
            game_id = api_game.get('GAME_ID')
            if game_id in game_ids_done:
                continue  # games are duplicated (fe: LAL:CHI -> CHI:LAL)
            try:
                game = Game.create_from_api_model(ApiGame(game_id))
                if game.season_type_id in ignore_season_types:
                    Log.info(f"Ignoring {game.matchup} because it's {game.season_type} type")
                    games_ignored.append(game_id)
                    continue
                Log.info(f"\t#{game_counter} Creating Play by Play records for game {game_id}: {game.matchup}")
                play_by_plays_records = ApiPlayByPlay.create_play_by_play_records(game_id=game.id,
                                                                                  home_team_id=game.home_team_id,
                                                                                  away_team_id=game.away_team_id,
                                                                                  home_team=game.home_team,
                                                                                  away_team=game.away_team,
                                                                                  game_date=game.game_date)
                Log.info(f"\t\tInserting {len(play_by_plays_records)} records for game {game.matchup}")
                for api_play_by_play in play_by_plays_records:
                    play_by_play = PlayByPlay.create_from_api_model(api_model=api_play_by_play)
                    play_by_play.persist()
                    records_added += 1
                    game_ids_done.append(game_id)
                Log.info(f"\t\t\t Done.")
            except (ValueError, AttributeError, IndexError) as ex:
                Log.error(f"Game {game_id} cant' be persisted. Ignoring")
                Log.error(', '.join(ex.args))
                games_ignored.append(game_id)
                continue
        end_time = datetime.datetime.now()
        Log.info(f"----- Season {season.name} done -----")
        Log.info(f"Start time: {start_time}")
        Log.info(f"End time: {end_time}")
        Log.info(f"Records added: {records_added}")
        Log.info(f"Games ignored: {', '.join(games_ignored)} ({len(games_ignored)}")

    @classmethod
    def get_season_player_shots(cls, season: Season):
        start_time = datetime.datetime.now()
        Log.info(f"Getting Player Shots data for all games in season {season}")
        shot_records_persisted = 0
        for team_index, team in enumerate(Team.fetch_all()):
            Log.info(f"\t#{team_index + 1}Team: {team.name}")
            players = ApiTeam.get_players(team_id=team.team_id, season=season)
            for player_index, player in enumerate(players):
                player_name = f"{player.get('PLAYER_FIRST_NAME')} {player.get('PLAYER_LAST_NAME')}"
                Log.info(f"\t\t #{player_index + 1} Player: {player_name}")
                player_id = player.get('PERSON_ID')
                shot_records = ApiPlayerSeasonShots.fetch_player_shots_records_from_nba(
                    player_id=player_id, team_id=team.team_id, season=season)
                Log.info(f"\t\t\tPersisting {len(shot_records)} shot records")
                for shot_record in shot_records:
                    api_player_shots = ApiPlayerSeasonShots(player_id=player_id, season=season,
                                                            shot_details=shot_record)
                    if api_player_shots:
                        player_shots_db = PlayerShots.create_from_api_model(api_player_shots)
                        player_shots_db.persist()
                        shot_records_persisted += 1
            Log.info(f"----- Team {team.name} done -----")
        end_time = datetime.datetime.now()
        Log.info(f"----- Season {season.name} done -----")
        Log.info(f"Start time: {start_time}")
        Log.info(f"End time: {end_time}")
        Log.info(f"Shot records persisted: {shot_records_persisted}")

    @staticmethod
    def get_data_from_timeframe(season_start: int, date_from: datetime, date_to: datetime):
        Crawler.get_data_for_season(season=Season(start_year=season_start), date_from=date_from, date_to=date_to)

    @staticmethod
    def get_data_beginning_from_recently_persisted():
        last_game_persisted = ApiGame.get_latest_game_persisted()
        date_from = last_game_persisted.game_date
        date_to = datetime.date.today()
        Crawler.get_data_for_season(season=Season(start_year=season_start), date_from=date_from, date_to=date_to)

    @staticmethod
    def get_data_from_yesterday():
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        Crawler.get_data_from_timeframe(season_start=2023, date_from=yesterday, date_to=today)


Database.recreate_database()
Crawler.persist_teams()


for season_start in [2023]:
    Crawler.get_data_for_season(season=Season(start_year=season_start))
    ignore_season_types = [SeasonType('003').season_id, SeasonType('001').season_id]  # ignoring all star and pre-season
    Crawler.get_play_by_play_data_for_season(season=Season(start_year=season_start),
                                             ignore_season_types=ignore_season_types)
    Crawler.get_season_player_shots(season=Season(start_year=season_start))

# Crawler.get_data_beginning_from_recently_persisted()
