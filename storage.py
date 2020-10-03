from abc import ABC, abstractmethod


class Storage(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def dataframe_to_csv(self, df, path):
        pass

    @abstractmethod
    def csv_to_dataframe(self, path):
        pass
