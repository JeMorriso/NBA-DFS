from abc import ABC, abstractmethod


class Sport:
    def __init__(self, start_date=None, season=None, categories=None):
        self.start_date = start_date
        # self.end_date = None
        self.season = season
        self.categories = categories

    @abstractmethod
    def get_boxscore(self, id):
        pass

    @abstractmethod
    def get_boxscores(self, date_):
        pass
