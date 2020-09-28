from datetime import datetime, date

import pytest

from nfl import NFL


@pytest.fixture
def nfl():
    return NFL()


@pytest.mark.parametrize('date_str, week', [('2020-09-10', 1), ('2020-09-11', 1), ('2020-09-19', 2), ('2021-01-03', 17)])
def test_week_from_date(nfl, date_str, week):
    date_ = datetime.strptime(date_str, '%Y-%m-%d').date()
    assert nfl._week_from_date(date_) == week
