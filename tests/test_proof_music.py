from peal.methods import find_method
from peal.music import runs_in, score
from peal.proof import prove
from peal.rows import Row


def test_repeated_row_is_reported():
    rows = [Row.parse("1234"), Row.parse("2143"), Row.parse("1234")]
    result = prove(rows)
    assert not result.is_true
    assert result.repeats[Row.parse("1234")] == [0, 2]


def test_runs():
    assert runs_in("12345678", 4) == [(i, "12345678"[i:i + 4]) for i in range(5)]
    assert runs_in("13248765", 4) == [(4, "8765")]


def test_score_counts_back_runs():
    tally = score(find_method("plain bob major").plain_course())
    assert tally["rounds"] == 1
    assert tally["back 4-runs"] > 0
