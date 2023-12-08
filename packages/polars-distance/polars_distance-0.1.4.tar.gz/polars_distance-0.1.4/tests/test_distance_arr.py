import pytest
import polars as pl
import polars_distance as pld
from polars.testing import assert_frame_equal


@pytest.fixture()
def data():
    return pl.DataFrame(
        {
            "arr": [[1, 2.0, 3.0, 4.0]],
            "arr2": [[10.0, 8.0, 5.0, 3.0]],
            "str_l": ["hello world"],
            "str_r": ["hela wrld"],
        },
        schema={
            "arr": pl.Array(inner=pl.Float64, width=4),
            "arr2": pl.Array(inner=pl.Float64, width=4),
            "str_l": pl.Utf8,
            "str_r": pl.Utf8,
        },
    )


def test_cosine(data):
    result = data.select(
        pld.col("arr").dist_arr.cosine("arr2").alias("dist_cosine"),
    )

    expected = pl.DataFrame(
        [
            pl.Series("dist_cosine", [0.31232593265732134], dtype=pl.Float64),
        ]
    )

    assert_frame_equal(result, expected)


def test_chebyshev(data):
    result = data.select(
        pld.col("arr").dist_arr.chebyshev("arr2").alias("dist_chebyshev"),
    )

    expected = pl.DataFrame(
        [
            pl.Series("dist_chebyshev", [9.0], dtype=pl.Float64),
        ]
    )

    assert_frame_equal(result, expected)


def test_canberra(data):
    result = data.select(
        pld.col("arr").dist_arr.canberra("arr2").alias("dist_canberra"),
    )

    expected = pl.DataFrame(
        [
            pl.Series("dist_canberra", [1.811038961038961], dtype=pl.Float64),
        ]
    )

    assert_frame_equal(result, expected)


def test_euclidean(data):
    result = data.select(
        pld.col("arr").dist_arr.euclidean("arr2").alias("dist_euclidean"),
    )

    expected = pl.DataFrame(
        [
            pl.Series("dist_euclidean", [11.045361017187261], dtype=pl.Float64),
        ]
    )

    assert_frame_equal(result, expected)


def test_hamming_str(data):
    result = data.select(
        pld.col("str_l").dist_str.hamming("str_r").alias("dist_hamming"),
    )

    expected = pl.DataFrame(
        [
            pl.Series("dist_hamming", [6], dtype=pl.UInt32),
        ]
    )

    assert_frame_equal(result, expected)


def test_levenshtein(data):
    result = data.select(
        pld.col("str_l").dist_str.levenshtein("str_r").alias("dist_levenshtein")
    )

    expected = pl.DataFrame(
        [
            pl.Series("dist_levenshtein", [3], dtype=pl.UInt32),
        ]
    )

    assert_frame_equal(result, expected)
