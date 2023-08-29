from data.player_stats_fetcher import PlayerGameStatsFetcher
from data.players_fetcher import PlayersFetcher
from data.team_stats_fetcher import TeamGameStatsFetcher
from data.teams_fetcher import TeamsFetcher


class DataFetcher:
    teams: TeamsFetcher = TeamsFetcher()
    players: PlayersFetcher = PlayersFetcher()
    team_game_stats: TeamGameStatsFetcher = TeamGameStatsFetcher()
    player_game_stats: PlayerGameStatsFetcher = PlayerGameStatsFetcher()

