from sportsreference.nfl.boxscore import Boxscore, Boxscores
from sportsreference.nfl.teams import Teams
from sportsreference.nfl.roster import Player
import pandas as pd

from srwrapper import SRWrapper
from utils import Utils


class NFLSportsReference(SRWrapper):
    def __init__(self, nfl_config):
        super().__init__(nfl_config)

    def _get_player_position(self, player):
        """Return a player's position, if it is one of self.offense_positions

        pro-football-reference only lists position in tables if the player was
        a starter. The player's position is meant to be stored in
        player.position, but for some reason, it is sometimes blank for
        important players (eg Deshaun Watson). Try and find the position.

        # TODO: what about players who have never started (eg Darwin Thompson)?

        Returns:
            player's position, or None

        """
        position = player.position
        if not position:
            # player._position is in reverse chronological order. Reverse the
            # list to get the player's most recent position.
            positions = [p.lower() for p in player._position[::-1]]
            for p in self.sport.positions:
                if p in positions:
                    position = p

        return position if position else None

    def get_boxscore(self, id):
        return Boxscore(id)

    def get_boxscores(self, date_):
        week = Utils._week_from_date(date_, self.sport.start_date)
        return Boxscores(week, self.sport.season).games[f"{week}-{self.sport.season}"]

    def get_player(self, id_):
        return Player(id_)

    def get_teams(self, season=None):
        return Teams(season)