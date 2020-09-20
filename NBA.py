from nba_api.stats.endpoints import boxscoretraditionalv2


class NBA:
    def __init__(self):
        self.start_date = None
        self.end_date = None

    def get_boxscore(self, game_id):
        pass
        # call NBA_API with game id
        # res.player_stats.get_data_frame()
        # return df

    def iterate_games(self, fn, fn_params=None, start_date=None, end_date=None):
        pass
        # call function for each game in range
        # return df
