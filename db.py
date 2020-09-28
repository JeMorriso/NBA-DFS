import os
from abc import ABC, abstractmethod


class DB(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def dataframe_to_sql(self, df):
        pass

    @abstractmethod
    def sql_to_dataframe(self, query, table):
        pass
