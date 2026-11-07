import pytest

from peal.rows import Row, RowError


def test_parse_and_str_round_trip():
    assert str(Row.parse("1234567890ET")) == "1234567890ET"


def test_rejects_non_permutation():
    with pytest.raises(RowError):
        Row.parse("1123")


def test_multiply_and_inverse():
    r = Row.parse("3142")
    assert (r * r.inverse()).is_rounds()
    assert r * Row.rounds(4) == r


def test_position_of():
    assert Row.parse("2413").position_of(0) == 2
