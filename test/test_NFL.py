from datetime import datetime, date

import pytest

from nfl import NFL


@pytest.fixture
def nfl():
    return NFL()


@pytest.mark.parametrize('date_str, week', [('2020-09-10', 1), ('2020-09-11', 1), ('2020-09-19', 2), ('2021-01-03', 17)])
def test_week_from_date(nfl, date_str, week):
    assert nfl._week_from_date(date.fromisoformat(date_str)) == week


@pytest.mark.parametrize('date_str, expected', [('2020-09-10', True)])
def test_get_boxscores(nfl, date_str, expected):
    assert nfl.get_boxscores(date.fromisoformat(date_str)) == expected


@pytest.mark.parametrize('date_str, expected', [('2020-09-10', True)])
def test_get_players_game_stats(nfl, date_str, expected):
    assert nfl.get_players_game_stats(
        date.fromisoformat(date_str)) == expected
