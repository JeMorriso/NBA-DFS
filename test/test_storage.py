import os

import pytest
import pandas as pd

from localstorage import LocalStorage


@pytest.fixture
def ls():
    return LocalStorage()


def test_csv_to_dataframe_local(ls):
    df = ls.csv_to_dataframe("input/fd-test-input.csv")
    assert len(df) > 1


def test_dataframe_to_csv_local(ls):
    df = ls.csv_to_dataframe("input/fd-test-input.csv")
    ls.dataframe_to_csv(df, "output/fd-test-output.csv")
    df2 = ls.csv_to_dataframe("input/fd-test-input.csv")
    assert df.equals(df2)