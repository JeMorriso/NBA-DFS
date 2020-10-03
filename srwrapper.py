from datetime import datetime

import pandas as pd


class SRWrapper:
    def __init__(self, sport):
        self.sport = sport

    def _update_stats_dict(self, players, sportsreference_id, stats):
        for p in players:
            stats.update(p.dataframe.to_dict("index"))
            stats[p.player_id]["sportsreference_id"] = sportsreference_id

    def _get_player_position(self, player):
        raise NotImplementedError()

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

    def get_players_game_stats(self, date_, categories=None):
        """
        Raises:
            KeyError: Error occurred accessing dict returned from
            self.get_boxscores()
        """

        stats = {}

        if categories is None:
            categories = self.sport.categories

        games = self.get_boxscores(date_)

        # TODO: change this back to games when done testing
        for g in games[:1]:
            game = self.get_boxscore(g["boxscore"])
            sportsreference_id = game._uri
            self._update_stats_dict(game.away_players, sportsreference_id, stats)
            self._update_stats_dict(game.home_players, sportsreference_id, stats)

        return pd.DataFrame.from_dict(stats, orient="index")[
            list(categories) + ["sportsreference_id"]
        ].fillna(0)

    def get_games_info(self, date_):
        games = self.get_boxscores(date_)

        games_info = {}
        for g in games:
            game_date = g["boxscore"][:8]
            game_date = datetime.strptime(game_date, "%Y%m%d").date().isoformat()
            games_info[g["boxscore"]] = {
                "home_name": g["home_name"],
                "away_name": g["away_name"],
                "date_": game_date,
            }

        return pd.DataFrame.from_dict(games_info, orient="index")

    def get_teams_info(self, season=None):
        # TODO: team names are not given atomically from sportsreference
        teams = self.get_teams(season)

        teams_info = {"name": [], "sportsreference_abbreviation": []}
        for team in teams:
            teams_info["name"].append(team.name)
            teams_info["sportsreference_abbreviation"].append(team.abbreviation)

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
