from abc import ABC, abstractmethod
import os
import time

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import StatementError


class DB(ABC):
    def __init__(self):
        self._temp_table = "temp_table"

    @property
    @abstractmethod
    def engine(self):
        pass

    @property
    @abstractmethod
    def startup_fn(self):
        pass

    @property
    def temp_table(self):
        return self._temp_table

    def dataframe_to_sql(
        self, df, table, if_exists="append", index=False, index_label=None
    ):
        """
        Raises:
            sqlalchemy.exc.IntegrityError: local database fail to append (fail
            uniqueness)
            sqlalchemy.exc.DatabaseError: aurora database fail to append (fail
            uniqueness)
        """
        self.startup_fn()
        df.to_sql(
            table,
            self.engine,
            if_exists=if_exists,
            index=index,
            index_label=index_label,
        )

    def sql_to_dataframe(self, query, params=None):
        """
        Args:
            query: the sql query. Note that the Aurora implementation DOES NOT SUPPORT
            renaming. The resulting dataframe seemingly always has the same column name
            as the table
            params: parameters to the sql query. Aurora implementation DOES NOT SUPPORT
            tuple parameters; throws Attribute error. Must use dict params.

        """
        self.startup_fn()
        return pd.read_sql(query, self.engine, params=params)

    def update_player_table(self, df):
        self.startup_fn()
        df.to_sql("temp_table", self.engine, if_exists="replace")
        query = """
            update player, temp_table
            set player.fanduel_id = temp_table.fanduel_id
            where player.id = temp_table.id
        """
        with self.engine.begin() as conn:
            conn.execute(query)

    def execute_query(self, query, params=None):
        """
        Returns:
            keys: List of column names in the query. LocalDB returns the correct names,
            (even if renamed) but the Aurora implementation always returns the original
            column names
        """
        with self.engine.begin() as conn:
            if params is None:
                rows = conn.execute(query).fetchall()
                keys = conn.execute(query).keys()
            else:
                rows = conn.execute(query, params).fetchall()
                keys = conn.execute(query, params).keys()
            return keys, rows


class AuroraDB(DB):
    def __init__(self, db):
        cluster_arn = os.getenv("CLUSTER_ARN")
        secret_arn = os.getenv("SECRET_ARN")
        self._engine = create_engine(
            f"mysql+auroradataapi://:@/{db}",
            echo=True,
            connect_args=dict(aurora_cluster_arn=cluster_arn, secret_arn=secret_arn),
        )
        self._startup_fn = self._cold_start

    @property
    def startup_fn(self):
        return self._startup_fn

    @property
    def engine(self):
        return self._engine

    def _cold_start(self):
        wait = 5
        tries = 10
        i = 0
        while i < tries:
            i += 1
            try:
                with self.engine.begin() as conn:
                    # dummy query to test if server is running
                    conn.execute("select 1;")
                return
            except StatementError:
                time.sleep(wait)

        raise Exception("Could not connect to serverless DB")


class LocalDB(DB):
    def __init__(self, db):
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        host = os.getenv("HOST")
        # TODO: self.engine in superclass?
        self._engine = create_engine(f"mysql+mysqldb://{user}:{password}@{host}/{db}")

    @property
    def startup_fn(self):
        # no startup required at this time
        return lambda *args: None

    @property
    def engine(self):
        return self._engine
