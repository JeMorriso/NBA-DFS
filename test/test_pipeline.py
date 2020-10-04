from datetime import date

import pytest

import local_pipeline
from model import Model
from localdb import LocalDB
from nfl import NFL
from nflsportsreference import NFLSportsReference
from localstorage import LocalStorage


@pytest.fixture
def nfl():
    return NFLSportsReference(NFL())


@pytest.fixture
def localdb_nfl():
    return LocalDB("nfl_dfs")


@pytest.fixture
def model():
    return Model()


@pytest.fixture
def localstorage():
    return LocalStorage()


@pytest.mark.parametrize("date_", [("2020-09-10")])
def test_local_nfl_insert_player_stats(nfl, localdb_nfl, date_):
    local_pipeline.insert_player_stats(nfl, localdb_nfl, date.fromisoformat(date_))


@pytest.mark.parametrize("input_csv", [("input/fd-test-input.csv")])
def test_local_nfl_match_players_with_csv(nfl, localdb_nfl, localstorage, input_csv):
    local_pipeline.match_players_with_csv(nfl, localdb_nfl, localstorage, input_csv)
