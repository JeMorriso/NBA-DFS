from datetime import date, timedelta, datetime

from sportsreference.nfl.boxscore import Boxscore, Boxscores
from sportsreference.nfl.teams import Teams
from sportsreference.nfl.roster import Player
import pandas as pd

from sport import Sport


class NFL(Sport):
    def __init__(self):
        categories = {
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
        super().__init__(
            start_date=date.fromisoformat("2020-09-10"),
            season=2020,
            categories=categories,
        )

        self.offense_positions = ["qb", "rb", "wr", "te"]

    def _week_from_date(self, date_):
        return int((date_ - self.start_date).days / 7) + 1

    def _update_stats_dict(self, players, sportsreference_id, stats):
        for p in players:
            stats.update(p.dataframe.to_dict("index"))
            stats[p.player_id]["sportsreference_id"] = sportsreference_id

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
            for p in self.offense_positions:
                if p in positions:
                    position = p

        return position if position else None

    def get_boxscore(self, id):
        return Boxscore(id)

    def get_boxscores(self, date_):
        # get the week from the date
        week = self._week_from_date(date_)
        return Boxscores(week, self.season)

    def get_players_game_stats(self, date_, categories=None):
        """
        Raises:
            KeyError: Error occurred accessing dict returned from
            self.get_boxscores()
        """

        stats = {}

        if categories is None:
            categories = self.categories

        games = self.get_boxscores(date_).games[
            f"{self._week_from_date(date_)}-{self.season}"
        ]

        # TODO: change this back to games when done testing
        for g in games[:1]:
            game = self.get_boxscore(g["boxscore"])
            sportsreference_id = game._uri
            self._update_stats_dict(game.away_players, sportsreference_id, stats)
            self._update_stats_dict(game.home_players, sportsreference_id, stats)

        return pd.DataFrame.from_dict(stats, orient="index")[
            list(self.categories) + ["sportsreference_id"]
        ].fillna(0)

    def get_games_info(self, date_):
        games = self.get_boxscores(date_).games[
            f"{self._week_from_date(date_)}-{self.season}"
        ]

        games_info = {}
        for g in games:
            # game_date = self.get_boxscore(g["boxscore"]).date
            game_date = g["boxscore"][:8]
            game_date = datetime.strptime(game_date, "%Y%m%d").date().isoformat()
            games_info[g["boxscore"]] = {
                "home_name": g["home_name"],
                "away_name": g["away_name"],
                "game_date": game_date,
            }

        return pd.DataFrame.from_dict(games_info, orient="index")

    def get_teams_info(self):
        teams = Teams()

        teams_info = {"name": [], "sportsreference_abbreviation": []}
        for team in teams:
            teams_info["name"].append(team.name)
            teams_info["sportsreference_abbreviation"].append(team.abbreviation)

        return pd.DataFrame.from_dict(teams_info)

    def get_player_info(self, sportsreference_id):
        player = Player(sportsreference_id)
        position = self._get_player_position(player)
        return (
            {"position": position, "name": player.name}
            if position is not None
            else None
        )

    def get_players_info(self, sportsreference_ids):
        players_info = {}

        for id_ in sportsreference_ids:
            player = self.get_player_info(id_)
            if player is not None:
                players_info[id_] = player

        return pd.DataFrame.from_dict(players_info, orient="index")
