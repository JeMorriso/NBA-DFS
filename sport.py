from abc import ABC, abstractmethod


class Sport:
    def __init__(self, start_date=None):
        self.start_date = start_date
        # self.end_date = None
        pass

    @abstractmethod
    def get_boxscore(self):
        pass

    @abstractmethod
    def get_boxscores(self, date_):
        pass
