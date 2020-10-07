from abc import ABC, abstractmethod
import os

import pandas as pd
from sqlalchemy import create_engine


class DB(ABC):
    def __init__(self):
        self._temp_table = "temp_table"

    @property
    @abstractmethod
    def engine(self):
        pass

    @property
    def temp_table(self):
        return self._temp_table

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


class AuroraDB(DB):
    def __init__(self, db):
        cluster_arn = os.getenv("CLUSTER_ARN")
        secret_arn = os.getenv("SECRET_ARN")
        self._engine = create_engine(
            f"mysql+auroradataapi://:@/{db}",
            echo=True,
            connect_args=dict(aurora_cluster_arn=cluster_arn, secret_arn=secret_arn),
        )

    @property
    def engine(self):
        return self._engine


class LocalDB(DB):
    def __init__(self, db):
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        host = os.getenv("HOST")
        # TODO: self.engine in superclass?
        self._engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}/{db}")

    @property
    def engine(self):
        return self._engine
