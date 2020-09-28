from abc import ABC, abstractmethod


class Storage:
    def __init__(self):
        pass

    @abstractmethod
    def to_csv(self, df, path):
        pass
