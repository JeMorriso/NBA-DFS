import os

import mysql.connector

from db import DB


class LocalDB(DB):
    def __init__(self):
        super().__init__()
        self.connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            user=os.getenv("USER"),
            database=os.getenv('DATABASE'),
            password=os.getenv('PASSWORD'))

    def dataframe_to_sql(self, df):
        pass

    def sql_to_dataframe(self, query, table):
        pass
