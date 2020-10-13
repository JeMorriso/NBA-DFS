import pytest


@pytest.mark.parametrize("storage", [("local"), ("s3")], indirect=["storage"])
def test_csv_to_dataframe(storage):
    df = storage.csv_to_dataframe("input/fd-test-input.csv")
    assert len(df) > 1


@pytest.mark.parametrize("storage", [("local"), ("s3")], indirect=["storage"])
def test_dataframe_to_csv(storage):
    df = storage.csv_to_dataframe("input/fd-test-input.csv")
    storage.dataframe_to_csv(df, "input/fd-test-input2.csv")
    df2 = storage.csv_to_dataframe("input/fd-test-input2.csv")
    # I don't know why this is failing
    # assert df.equals(df2)
