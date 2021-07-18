import pytest
import pandas as pd
import pandas.testing as pdt

import pandas_tab  # noqa: F401

nan = float("nan")


@pytest.fixture
def df() -> pd.DataFrame:
    return pd.DataFrame({
        "foo":  ["a", "a", "b", "a", "b", "c", "a"],
        "bar":  [4,   5,   7,   6,   7,   7,   5],
        "fizz": [12,  63,  23,  36,  21,  28,  42]
    })


def test_one_way_simple(df: pd.DataFrame):
    output_df = df.tab("foo")

    expected_df = pd.DataFrame(
        {
            "size": [4, 2, 1],
            "percent": [57.14, 28.57, 14.29]
        },
        index=pd.Index(["a", "b", "c"], name="foo")
    )

    pdt.assert_frame_equal(output_df, expected_df)


def test_two_way_simple(df: pd.DataFrame):
    output_df = df.tab("foo", "bar")

    expected_df = pd.DataFrame(
        [
            [1, 2, 1, 0],
            [0, 0, 0, 2],
            [0, 0, 0, 1]
        ],
        index=pd.Index(["a", "b", "c"], name="foo"),
        columns=pd.Index([4, 5, 6, 7], name="bar")
    )

    pdt.assert_frame_equal(output_df, expected_df)


def test_one_way_agg(df: pd.DataFrame):
    output_df = df.tab("foo", values="fizz", aggfunc=pd.Series.mean)

    expected_df = pd.DataFrame(
        {"mean": [38.25, 22.0, 28.0]},
        index=pd.Index(["a", "b", "c"], name="foo")
    )

    pdt.assert_frame_equal(output_df, expected_df)


def test_two_way_agg(df: pd.DataFrame):
    output_df = df.tab("foo", "bar", values="fizz", aggfunc=pd.Series.mean)

    expected_df = pd.DataFrame(
        [
            [12.0, 52.5, 36.0, nan],
            [nan,  nan,  nan,  22.0],
            [nan,  nan,  nan,  28.0]
        ],
        index=pd.Index(["a", "b", "c"], name="foo"),
        columns=pd.Index([4, 5, 6, 7], name="bar")
    )

    pdt.assert_frame_equal(output_df, expected_df)
