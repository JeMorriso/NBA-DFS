from datetime import date

import pytest

from nba import NBA
from nbasportsreference import NBASportsReference
from utils import Utils


@pytest.fixture
def nba():
    return NBASportsReference(NBA())


@pytest.mark.parametrize("date_str, num_games", [("2019-10-22", 2)])
def test_get_boxscores(nba, date_str, num_games):
    date_ = date.fromisoformat(date_str)
    boxscores = nba.get_boxscores(date_)
    assert len(boxscores) == num_games


@pytest.mark.parametrize("date_str", [("2019-10-22")])
def test_get_players_game_stats(nba, date_str):
    df = nba.get_players_game_stats(date.fromisoformat(date_str))

    assert len(df) > 1
    # + 1 because of sportsreference_id
    assert len(df.columns) == len(nba.sport.categories) + 1


@pytest.mark.parametrize("date_str", [("2019-10-22")])
def test_get_games_info(nba, date_str):
    df = nba.get_games_info(date.fromisoformat(date_str))

    assert len(df) == 2
    assert len(df.columns) == 3


def test_get_teams(nba):
    df = nba.get_teams_info(season=2019)

    assert len(df) == 30


@pytest.mark.parametrize("date_str", [("2019-10-22")])
def test_get_players_info(nba, date_str):
    df = nba.get_players_game_stats(date.fromisoformat(date_str))

    df2 = nba.get_players_info(df.index.tolist())
    df = df.loc[df2.index.tolist()]

    assert len(df) == len(df2)
