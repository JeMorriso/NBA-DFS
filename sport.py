from abc import ABC, abstractmethod


class Sport:
    def __init__(self):
        # self.start_date = None
        # self.end_date = None
        pass

    @abstractmethod
    def get_boxscore(self):
        pass
