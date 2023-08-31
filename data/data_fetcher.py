from data.play_by_play_fetcher import PlayByPlayFetcher
from data.player_shots_fetcher import PlayerShotsFetcher
from data.player_stats_fetcher import PlayerGameStatsFetcher
from data.players_fetcher import PlayersFetcher
from data.team_stats_fetcher import TeamGameStatsFetcher
from data.teams_fetcher import TeamsFetcher


class DataFetcher:
    teams: TeamsFetcher = TeamsFetcher()
    players: PlayersFetcher = PlayersFetcher()
    team_game_stats: TeamGameStatsFetcher = TeamGameStatsFetcher()
    player_game_stats: PlayerGameStatsFetcher = PlayerGameStatsFetcher()
    play_by_play: PlayByPlayFetcher = PlayByPlayFetcher()
    player_shots: PlayerShotsFetcher = PlayerShotsFetcher()

