from sportsreference.nba.boxscore import Boxscore, Boxscores
from sportsreference.nba.teams import Teams
from sportsreference.nba.roster import Player
import pandas as pd

from srwrapper import SRWrapper
from utils import Utils


class NBASportsReference(SRWrapper):
    def __init__(self, nba_config):
        super().__init__(nba_config)

    def _get_player_position(self, player):
        return player.position

    def get_boxscore(self, id):
        return Boxscore(id)

    def get_boxscores(self, date_):
        return Boxscores(date_).games[Utils._date_to_sportsreference_str(date_)]

    def get_player(self, id_):
        return Player(id_)

    def get_teams(self, season=None):
        return Teams(season)
