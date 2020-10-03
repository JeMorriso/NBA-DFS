import os

import pytest
import pandas as pd
from sqlalchemy.exc import IntegrityError

from localdb import LocalDB
from nflsportsreference import NFLSportsReference
from nfl import NFL


@pytest.fixture
def nfl_local():
    return LocalDB(os.getenv("NFL_DATABASE"))


@pytest.fixture
def nfl():
    return NFLSportsReference(NFL())


def test_nfl_local_init(nfl_local):
    pass


def test_to_dataframe(nfl_local):
    df = nfl_local.sql_to_dataframe("select * from teams")
    print(df.head())


def test_to_sql_duplicate(nfl_local):
    d = {"sportsreference_abbreviation": ["htx"], "name": ["Houston Texans"]}
    df = pd.DataFrame(data=d)
    try:
        nfl_local.dataframe_to_sql(df, "team", index=False, if_exists="append")
        nfl_local.dataframe_to_sql(df, "team", index=False, if_exists="append")
        pytest.fail("should not insert duplicate")
    except IntegrityError:
        pass


def test_insert_teams(nfl_local, nfl):
    df = nfl.get_teams_info()
    nfl_local.dataframe_to_sql(df, "team", index=False)
    df2 = nfl_local.sql_to_dataframe("select * from team")
    assert len(df) == len(df2)
