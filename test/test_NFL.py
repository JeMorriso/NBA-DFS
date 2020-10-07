from datetime import date

import pytest

from utils import TimeInterval


@pytest.mark.parametrize(
    "date_str, week",
    [("2020-09-10", 1), ("2020-09-11", 1), ("2020-09-19", 2), ("2021-01-03", 17)],
)
def test_week_from_date(utils, date_str, week):
    start_date = date.fromisoformat("2020-09-10")
    assert utils._week_from_date(date.fromisoformat(date_str), start_date) == week


@pytest.mark.parametrize(
    "s, e, exp1, exp2",
    [
        ("2020-09-10", "2020-09-11", 1, 1),
        ("2020-09-10", "2020-09-17", 7, 1),
        ("2020-09-10", "2020-09-18", 8, 2),
    ],
)
def test_date_range(utils, s, e, exp1, exp2):
    range_ = utils._date_range(date.fromisoformat(s), date.fromisoformat(e))
    assert len(range_) == exp1
    range_ = utils._date_range(
        date.fromisoformat(s), date.fromisoformat(e), interval=TimeInterval.WEEK
    )
    assert len(range_) == exp2


@pytest.mark.parametrize(
    "nfl, date_str, num_games",
    [("day", "2020-09-10", 1), ("week", "2020-09-10", 16)],
    indirect=["nfl"],
)
def test_get_boxscores(nfl, date_str, num_games):
    date_ = date.fromisoformat(date_str)
    boxscores = nfl.get_boxscores_fn(date_)
    assert len(boxscores) == num_games


@pytest.mark.parametrize(
    "nfl, date_str", [("day", "2020-09-10"), ("week", "2020-09-10")], indirect=["nfl"]
)
def test_get_players_game_stats(nfl, date_str):
    df = nfl.get_players_game_stats(date.fromisoformat(date_str))

    assert len(df) > 1
    # + 1 because of sportsreference_id
    assert len(df.columns) == len(nfl.categories) + 1


@pytest.mark.parametrize(
    "nfl, s, e",
    [("day", "2020-09-10", "2020-10-06"), ("week", "2020-09-10", "2020-09-17")],
    indirect=["nfl"],
)
def test_get_players_game_stats_range(utils, nfl, s, e):
    for date_ in utils._date_range(
        date.fromisoformat(s),
        date.fromisoformat(e),
        nfl.time_interval,
    ):
        df = nfl.get_players_game_stats(date_)
        if not df.empty:
            assert len(df.columns) == len(nfl.categories) + 1


@pytest.mark.parametrize("nfl, date_str", [("week", "2020-09-10")], indirect=["nfl"])
def test_get_games_info(nfl, date_str):
    df = nfl.get_games_info(date.fromisoformat(date_str))

    assert len(df) == 16
    assert len(df.columns) == 3


@pytest.mark.parametrize(
    "nfl, s, e, exp",
    [("day", "2020-09-10", "2020-10-06", 1), ("week", "2020-09-10", "2020-10-06", 8)],
    indirect=["nfl"],
)
def test_get_games_info_range(utils, nfl, nfl_day, s, e, exp):

    for date_ in utils._date_range(
        date.fromisoformat(s),
        date.fromisoformat(e),
        nfl.time_interval,
    ):
        df = nfl.get_games_info(date_)
        if not df.empty:
            # bye weeks mean some weeks have less than 16 games
            assert len(df) >= exp
            assert len(df.columns) == 3


def test_get_teams(nfl_default):
    df = nfl_default.get_teams_info()

    assert len(df) == 32


@pytest.mark.parametrize("date_str", [("2020-09-10")])
def test_get_players_info(nfl_default, date_str):
    df = nfl_default.get_players_game_stats(date.fromisoformat(date_str))

    df2 = nfl_default.get_players_info(df.index.tolist())
    df = df.loc[df2.index.tolist()]

    assert len(df) == len(df2)


@pytest.mark.parametrize(
    "nfl, s, e",
    [("day", "2020-09-10", "2020-09-17"), ("week", "2020-09-10", "2020-09-17")],
    indirect=["nfl"],
)
def test_get_players_info_range(utils, nfl, s, e):
    for date_ in utils._date_range(
        date.fromisoformat(s),
        date.fromisoformat(e),
        nfl.time_interval,
    ):
        df = nfl.get_players_game_stats(date_)
        df2 = nfl.get_players_info(df.index.tolist())
        df = df2.loc[df2.index.tolist()]
