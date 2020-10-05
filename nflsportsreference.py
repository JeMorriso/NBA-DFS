import json
import os
from datetime import date

from sportsreference.nfl.boxscore import Boxscore, Boxscores
from sportsreference.nfl.teams import Teams
from sportsreference.nfl.roster import Player, Roster

from srwrapper import SRWrapper
from utils import Utils


class NFLSportsReference(SRWrapper):
    def __init__(self, get_boxscores_fn=None):
        self._categories = {
            "completed_passes",
            "attempted_passes",
            "passing_yards",
            "passing_touchdowns",
            "interceptions_thrown",
            "times_sacked",
            "quarterback_rating",
            "rush_attempts",
            "rush_yards",
            "rush_touchdowns",
            "times_pass_target",
            "receptions",
            "receiving_yards",
            "receiving_touchdowns",
            "kickoff_return_touchdown",
            "punt_return_touchdown",
            "fumbles_lost",
            "fumbles_recovered_for_touchdown",
            "field_goals_made",
            "extra_points_made",
        }
        self._start_date = date.fromisoformat("2020-09-10")
        self._season = 2020
        self._positions = ["QB", "RB", "WR", "TE"]

        with open(
            os.getcwd() + "/json/nfl_sportsreference_team_abbreviations.json", "r"
        ) as f:
            self._abbreviations = json.load(f)

        self._abbreviations_inverted = {v: k for k, v in self.abbreviations.items()}

        self._get_boxscores_fn = (
            self.get_boxscores_by_week if get_boxscores_fn is None else get_boxscores_fn
        )

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
        return self._abbreviations

    @property
    def abbreviations_inverted(self):
        return self._abbreviations_inverted

    @property
    def get_boxscores_fn(self):
        return self._get_boxscores_fn

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
            positions = [p.upper() for p in player._position[::-1]]
            for p in self.positions:
                if p in positions:
                    position = p

        return position.upper() if position else None

    def get_boxscore(self, id):
        return Boxscore(id)

    def get_boxscores(self, date_):
        week = Utils._week_from_date(date_, self.start_date)
        boxscores = Boxscores(week, self.season).games[f"{week}-{self.season}"]
        return [
            b
            for b in boxscores
            if self._boxscore_id_to_date(b["boxscore"]) == date_.isoformat()
        ]

    def get_boxscores_by_week(self, date_):
        week = Utils._week_from_date(date_, self.start_date)
        return Boxscores(week, self.season).games[f"{week}-{self.season}"]

    def get_player(self, id_):
        return Player(id_)

    def get_teams(self, season=None):
        return Teams(season)

    def get_roster(self, team, season=None, slim=False):
        return Roster(team, year=season, slim=slim)
