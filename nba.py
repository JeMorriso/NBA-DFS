from nba_api.stats.endpoints import boxscoretraditionalv2, leaguegamefinder, leaguegamelog
from datetime import date, timedelta

from sport import Sport


class NBA(Sport):
    def __init__(self):
        Sport.__init__(self)
        # self.start_date = None
        # self.end_date = None

    def get_boxscore(self, game_id):
        pass
        # call NBA_API with game id
        # res.player_stats.get_data_frame()
        # return df

    def get_boxscores(self, date_):
        pass

    def iterate_games(self, fn, fn_params=None, start_date=None, end_date=None):
        # default to most recent games played, assuming script is running sometime the next day (UTC)
        if start_date == None:
            start_date = date.today() - timedelta(days=1)
        if end_date == None:
            end_date = date.today()

        # using '.get_data_frames()[0]' from 'Finding Games' example on nba_api github repo
        # games_in_range = leaguegamefinder.LeagueGameFinder(
        #     date_from_nullable='2019-10-30', date_to_nullable='2019-10-31').get_data_frames()[0]
        games_in_range = leaguegamelog.LeagueGameLog(
            date_from_nullable='2019-10-30', date_to_nullable='2019-10-31').get_data_frames()[0]
        # games = leaguegamefinder.LeagueGameFinder(
        #     team_id_nullable='1610612738').get_data_frames()[0]

        print('what')

        # call function for each game in range
        # return df
