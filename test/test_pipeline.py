from datetime import date

import pytest
import pandas as pd

import pipeline


@pytest.mark.parametrize(
    "start_date, end_date, db",
    [
        ("2020-09-10", "2020-09-11", "local"),
        ("2020-09-10", "2020-09-11", "aurora"),
        (None, None, "local"),
        (None, None, "aurora"),
    ],
    indirect=["db"],
)
def test_insert_player_stats(nfl_default, db, start_date, end_date):
    if start_date is not None:
        start_date = date.fromisoformat(start_date)
    if end_date is not None:
        end_date = date.fromisoformat(end_date)
    pipeline.insert_player_stats(
        nfl_default, db, start_date=start_date, end_date=end_date
    )


@pytest.mark.parametrize(
    "start_date, end_date, db, nfl",
    [
        ("2020-09-10", "2020-09-11", "local", "day"),
        ("2020-09-10", "2020-09-11", "aurora", "day"),
        (None, None, "local", "day"),
        (None, None, "aurora", "day"),
        ("2020-10-08", "2020-10-09", "aurora", "day"),
        ("2020-10-08", "2020-10-09", "local", "day"),
    ],
    indirect=["db", "nfl"],
)
def test_insert_player_stats_by_day(db, nfl, start_date, end_date):
    if start_date is not None:
        start_date = date.fromisoformat(start_date)
    if end_date is not None:
        end_date = date.fromisoformat(end_date)
    pipeline.insert_player_stats(nfl, db, start_date=start_date, end_date=end_date)


def test_local_driver_fn(nfl, localdb_nfl, model, localstorage):
    pipeline.driver_fn(
        nfl, localdb_nfl, model, localstorage, "/input/fd-test-input.csv", None
    )


@pytest.mark.parametrize(
    "input_csv, db, storage",
    [
        ("/input/fd-test-input.csv", "local", "local"),
        ("/input/fd-test-input.csv", "aurora", "local"),
    ],
    indirect=["db", "storage"],
)
def test_match_players_with_csv(nfl_default, db, storage, input_csv):
    fanduel_players = pipeline.clean_fanduel_players(
        storage.csv_to_dataframe(input_csv)
    )
    pipeline.match_players_with_csv(nfl_default, db, storage, fanduel_players)


@pytest.mark.parametrize(
    "db, storage", [("local", "local"), ("aurora", "local")], indirect=["db", "storage"]
)
def test_model_and_output_to_csv(db, model, storage):
    fanduel_players = pipeline.clean_fanduel_players(
        storage.csv_to_dataframe("/input/fd-test-input.csv")
    )
    pipeline.model_and_output_to_csv(
        db, model, storage, "/output/fd-test-output.csv", fanduel_players
    )
