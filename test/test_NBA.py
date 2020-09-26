from nba import NBA
import pytest


@pytest.fixture
def nba():
    return NBA()


def test_iterate_games(nba):
    nba.iterate_games(None)
