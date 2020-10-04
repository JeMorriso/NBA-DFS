import os

from sqlalchemy import create_engine
import pandas as pd

from db import DB


class LocalDB(DB):
    def __init__(self, db):
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        host = os.getenv("HOST")
        # TODO: self.engine in superclass?
        self.engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}/{db}")
        self.temp_table = "temp_table"

    def dataframe_to_sql(
        self, df, table, if_exists="append", index=False, index_label=None
    ):
        df.to_sql(
            table,
            self.engine,
            if_exists=if_exists,
            index=index,
            index_label=index_label,
        )

    def sql_to_dataframe(self, query, params=None):
        return pd.read_sql(query, self.engine, params=params)

    def update_player_table(self, df):
        df.to_sql("temp_table", self.engine, if_exists="replace")
        query = """
            update player, temp_table
            set player.fanduel_id = temp_table.fanduel_id
            where player.id = temp_table.id
        """
        with self.engine.begin() as conn:
            conn.execute(query)
