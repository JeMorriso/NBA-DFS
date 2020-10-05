from datetime import date

from sportsreference.nba.boxscore import Boxscore, Boxscores
from sportsreference.nba.teams import Teams
from sportsreference.nba.roster import Player, Roster

from srwrapper import SRWrapper
from utils import Utils


class NBASportsReference(SRWrapper):
    def __init__(self, nba_config):
        self._categories = {
            "assists",
            "blocks",
            "defensive_rating",
            "defensive_rating",
            "defensive_rebounds",
            "field_goal_attempts",
            "field_goals",
            "free_throw_attempts",
            "free_throws",
            "minutes_played",
            "offensive_rating",
            "offensive_rebounds",
            "personal_fouls",
            "points",
            "steals",
            "three_point_attempts",
            "three_pointers",
            "total_rebounds",
            "turnovers",
            "two_point_attempts",
            "two_pointers",
        }
        self._start_date = date.fromisoformat("2019-10-22")
        self._season = 2019
        self._positions = ["PG", "SG", "SF", "PF", "C"]

        self._get_boxscores_fn = self.get_boxscores

    @property
    def categories(self):
        return self._categories

    @property
    def start_date(self):
        return self._start_date

    @property
    def season(self):
        return self._season

    @property
    def positions(self):
        return self._positions

    @property
    def abbreviations(self):
        return None

    @property
    def abbreviations_inverted(self):
        return None

    @property
    def get_boxscores_fn(self):
        return self._get_boxscores_fn

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

    def get_roster(self, team, season=None, slim=False):
        return Roster(team, year=season, slim=slim)
