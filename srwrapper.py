from datetime import datetime
from abc import ABC, abstractmethod

import pandas as pd


class SRWrapper(ABC):
    @property
    @abstractmethod
    def categories(self):
        pass

    @property
    @abstractmethod
    def start_date(self):
        pass

    @property
    @abstractmethod
    def season(self):
        pass

    @property
    @abstractmethod
    def positions(self):
        pass

    @property
    @abstractmethod
    def abbreviations(self):
        pass

    @property
    @abstractmethod
    def abbreviations_inverted(self):
        pass

    @property
    @abstractmethod
    def get_boxscores_fn(self):
        pass

    @property
    @abstractmethod
    def time_interval(self):
        pass

    @abstractmethod
    def _get_player_position(self, player):
        pass

    @abstractmethod
    def get_boxscore(self, id_):
        pass

    @abstractmethod
    def get_boxscores(self, date_):
        pass

    @abstractmethod
    def get_player(self, id_):
        pass

    @abstractmethod
    def get_teams(self, season):
        pass

    @abstractmethod
    def get_roster(self, team, season):
        pass

    def _boxscore_id_to_date(self, id_):
        return datetime.strptime(id_[:8], "%Y%m%d").date().isoformat()

    def _update_stats_dict(self, players, game_id, stats):
        for p in players:
            stats.update(p.dataframe.to_dict("index"))
            stats[p.player_id]["game_id"] = game_id

    def get_players_game_stats(self, date_):
        """
        Raises:
            KeyError: Error occurred accessing dict returned from
            self.get_boxscores()
        """
        stats = {}

        games = self.get_boxscores_fn(date_)

        # TODO
        for g in games:
            game = self.get_boxscore(g["boxscore"])
            game_id = game._uri
            self._update_stats_dict(game.away_players, game_id, stats)
            self._update_stats_dict(game.home_players, game_id, stats)

        return pd.DataFrame.from_dict(stats, orient="index")[
            list(self.categories) + ["game_id"]
        ].fillna(0)

    def get_games_info(self, date_):
        games = self.get_boxscores_fn(date_)

        # TODO
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
