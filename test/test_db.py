import pytest
import pandas as pd
from sqlalchemy.exc import IntegrityError, DatabaseError


@pytest.mark.parametrize("db", [("local"), ("aurora")], indirect=["db"])
def test_to_dataframe(db):
    df = db.sql_to_dataframe("select * from team")
    assert len(df) == 32


@pytest.mark.parametrize("db", [("local"), ("aurora")], indirect=["db"])
def test_to_sql_duplicate(db):
    d = {"abbreviation": ["htx"], "name": ["Houston Texans"]}
    df = pd.DataFrame(data=d)
    try:
        db.dataframe_to_sql(df, "team", index=False, if_exists="append")
        db.dataframe_to_sql(df, "team", index=False, if_exists="append")
        pytest.fail("should not insert duplicate")
    except IntegrityError:
        pass
    except DatabaseError:
        pass


@pytest.mark.parametrize(
    "db, nfl", [("local", "week"), ("aurora", "week")], indirect=["db", "nfl"]
)
def test_insert_teams(db, nfl):
    df = nfl.get_teams_info()
    db.dataframe_to_sql(df, "team", index=False)
    df2 = db.sql_to_dataframe("select * from team")
    assert len(df) == len(df2)
