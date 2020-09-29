from datetime import date, timedelta, datetime

from sportsreference.nfl.boxscore import Boxscore, Boxscores
import pandas as pd

from sport import Sport


class NFL(Sport):
    def __init__(self):
        categories = {'completed_passes', 'attempted_passes', 'passing_yards', 'passing_touchdowns', 'interceptions_thrown', 'times_sacked', 'quarterback_rating', 'rush_attempts', 'rush_yards', 'rush_touchdowns',
                      'times_pass_target', 'receptions', 'receiving_yards', 'receiving_touchdowns', 'kickoff_return_touchdown', 'punt_return_touchdown', 'fumbles_lost', 'fumbles_recovered_for_touchdown', 'field_goals_made', 'extra_points_made'}
        Sport.__init__(self, start_date=date.fromisoformat(
            '2020-09-10'), season=2020, categories=categories)

    def _week_from_date(self, date_):
        return int((date_ - self.start_date).days / 7) + 1

    def _update_stats_dict(self, players, sportsreference_id, stats):
        for p in players:
            stats.update(p.dataframe.to_dict('index'))
            stats[p.player_id]['sportsreference_id'] = sportsreference_id

    def get_boxscore(self, id):
        return Boxscore(id)

    def get_boxscores(self, date_):
        # get the week from the date
        week = self._week_from_date(date_)
        return Boxscores(week, self.season)

    def get_players_game_stats(self, date_, categories=None):
        """
        Raises:
            KeyError: Error occurred accessing dict returned from self.get_boxscores()
        """

        stats = {}

        if categories is None:
            categories = self.categories

        games = self.get_boxscores(
            date_).games[f'{self._week_from_date(date_)}-{self.season}']

        for g in games:
            game = self.get_boxscore(g['boxscore'])
            sportsreference_id = game._uri
            self._update_stats_dict(
                game.away_players, sportsreference_id, stats)
            self._update_stats_dict(
                game.home_players, sportsreference_id, stats)

        return pd.DataFrame.from_dict(stats, orient='index')[list(categories)]

    def get_games_info(self, date_):
        games = self.get_boxscores(
            date_).games[f'{self._week_from_date(date_)}-{self.season}']

        for g in games:
            pass
