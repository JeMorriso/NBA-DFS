from datetime import datetime
from enum import Enum

import pandas as pd


class SRWrapper:
    def __init__(self, sport, abbreviations, get_boxscores_default):
        self.sport = sport
        # key: actual abbrev, value: sportsref abbrev
        self.abbreviations = abbreviations
        self.abbreviations_inverted = {v: k for k, v in abbreviations.items()}
        self.get_boxscores_default = get_boxscores_default

    def _update_stats_dict(self, players, game_id, stats):
        for p in players:
            stats.update(p.dataframe.to_dict("index"))
            stats[p.player_id]["game_id"] = game_id

    def _get_player_position(self, player):
        raise NotImplementedError()

    def _boxscore_id_to_date(self, id_):
        return datetime.strptime(id_[:8], "%Y%m%d").date().isoformat()

    def get_boxscore(self, id_):
        raise NotImplementedError()

    def get_boxscores(self, date_):
        raise NotImplementedError()

    def get_player(self, id_):
        raise NotImplementedError()

    def get_teams(self, season):
        raise NotImplementedError()

    def get_roster(self, team, season):
        raise NotImplementedError()

    def get_players_game_stats(self, date_, categories=None, get_boxscores=None):
        """
        Raises:
            KeyError: Error occurred accessing dict returned from
            self.get_boxscores()
        """

        if get_boxscores is None:
            get_boxscores = self.get_boxscores_default

        if categories is None:
            categories = self.sport.categories

        stats = {}

        games = get_boxscores(date_)

        for g in games:
            game = self.get_boxscore(g["boxscore"])
            game_id = game._uri
            self._update_stats_dict(game.away_players, game_id, stats)
            self._update_stats_dict(game.home_players, game_id, stats)

        return pd.DataFrame.from_dict(stats, orient="index")[
            list(categories) + ["game_id"]
        ].fillna(0)

    def get_games_info(self, date_, get_boxscores=None):
        if get_boxscores is None:
            get_boxscores = self.get_boxscores_default

        games = get_boxscores(date_)

        games_info = {}
        for g in games:
            game_date = self._boxscore_id_to_date(g["boxscore"])
            games_info[g["boxscore"]] = {
                "home_abbreviation": self.abbreviations_inverted[
                    g["home_abbr"].upper()
                ],
                "away_abbreviation": self.abbreviations_inverted[
                    g["away_abbr"].upper()
                ],
                "date_": game_date,
            }

        return pd.DataFrame.from_dict(games_info, orient="index")

    def get_teams_info(self, season=None):
        # TODO: team names are not given atomically from sportsreference
        teams = self.get_teams(season)

        teams_info = {"name": [], "abbreviation": []}
        for team in teams:
            teams_info["name"].append(team.name)
            teams_info["abbreviation"].append(
                self.abbreviations_inverted[team.abbreviation]
            )

        return pd.DataFrame.from_dict(teams_info)

    def get_player_info(self, sportsreference_id):
        # TODO: player names are not given atomically from sportsreference
        player = self.get_player(sportsreference_id)
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
