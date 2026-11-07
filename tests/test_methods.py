import pytest

from peal.methods import LIBRARY, find_method
from peal.proof import prove


@pytest.mark.parametrize(
    "title, lead_head, course_length",
    [
        ("Plain Bob Doubles", "13524", 40),
        ("Plain Bob Minor", "135264", 60),
        ("Cambridge Surprise Minor", "156342", 120),
        ("Cambridge Surprise Major", "15738264", 224),
    ],
)
def test_known_methods(title, lead_head, course_length):
    m = find_method(title)
    assert str(m.lead_head()) == lead_head
    assert len(m.plain_course()) == course_length


@pytest.mark.parametrize("method", LIBRARY, ids=lambda m: m.title)
def test_every_plain_course_is_true(method):
    assert prove(method.plain_course()).is_true


def test_treble_is_the_hunt_bell():
    assert find_method("plain bob major").hunt_bells() == [0]


def test_lookup_is_forgiving_about_case_and_spaces():
    assert find_method("  cambridge   SURPRISE minor ").stage == 6


def test_unknown_method():
    with pytest.raises(KeyError):
        find_method("Stedman Triples")
