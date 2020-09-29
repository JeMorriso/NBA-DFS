from datetime import datetime, date

import pytest

from nfl import NFL


@pytest.fixture
def nfl():
    return NFL()


@pytest.mark.parametrize('date_str, week', [('2020-09-10', 1), ('2020-09-11', 1), ('2020-09-19', 2), ('2021-01-03', 17)])
def test_week_from_date(nfl, date_str, week):
    assert nfl._week_from_date(date.fromisoformat(date_str)) == week


@pytest.mark.parametrize('date_str, num_games', [('2020-09-10', 16)])
def test_get_boxscores(nfl, date_str, num_games):
    date_ = date.fromisoformat(date_str)
    boxscores = nfl.get_boxscores(date_)
    assert len(
        boxscores.games[f'{nfl._week_from_date(date_)}-{nfl.season}']) == num_games


@pytest.mark.parametrize('date_str', [('2020-09-10')])
def test_get_players_game_stats(nfl, date_str):
    df = nfl.get_players_game_stats(
        date.fromisoformat(date_str))

    assert len(df) > 1
    # + 1 because of sportsreference_id
    assert len(df.columns) == len(nfl.categories) + 1


@pytest.mark.parametrize('date_str', [('2020-09-10')])
def test_get_games_info(nfl, date_str):
    df = nfl.get_games_info(
        date.fromisoformat(date_str))

    assert len(df) > 1
    # + 1 because of sportsreference_id
    assert len(df.columns) == len(nfl.categories) + 1
