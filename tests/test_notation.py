import pytest

from peal.notation import Change, PlaceNotationError, parse, to_string
from peal.rows import Row


def strs(changes):
    return [str(c) for c in changes]


def test_external_places_are_implied():
    assert str(Change(6, [1])) == "12"
    assert str(Change(6, [2])) == "36"
    assert str(Change(5, [0])) == "1"
    assert str(Change(5, [1, 2])) == "123"


def test_internal_gap_must_be_even():
    with pytest.raises(PlaceNotationError):
        Change(6, [0, 2])


def test_cross_on_odd_stage_fails():
    with pytest.raises(PlaceNotationError):
        Change(5, [])


def test_comma_form_is_palindromic():
    assert strs(parse("x16x16x16,12", 6)) == ["x", "16", "x", "16", "x", "16", "x", "16", "x", "16", "x", "12"]


def test_ampersand_form():
    assert strs(parse("&5.1.5.1.5,+125", 5)) == ["5", "1", "5", "1", "5", "1", "5", "1", "5", "125"]


def test_apply_cross():
    assert str(Change(4, []).apply(Row.rounds(4))) == "2143"


def test_bad_character():
    with pytest.raises(PlaceNotationError):
        parse("x1?x", 6)


def test_to_string():
    assert to_string(parse("x16x12", 6)) == "x16x12"
    assert to_string(parse("5.1.5", 5)) == "5.1.5"
