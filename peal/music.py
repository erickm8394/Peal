from collections import Counter

from .rows import BELL_CHARS


def _named_rows(stage):
    bells = BELL_CHARS[:stage]
    odds, evens = bells[0::2], bells[1::2]
    first, second = bells[:(stage + 1) // 2], bells[(stage + 1) // 2:]
    tittums = "".join(a + b for a, b in zip(first, second)) + first[len(second):]
    named = {
        "rounds": bells,
        "backrounds": bells[::-1],
        "queens": odds + evens,
        "kings": odds[::-1] + evens,
        "tittums": tittums,
    }
    return named


def runs_in(row_text, length):
    found = []
    for i in range(len(row_text) - length + 1):
        chunk = row_text[i:i + length]
        idx = [BELL_CHARS.index(c) for c in chunk]
        diffs = {b - a for a, b in zip(idx, idx[1:])}
        if diffs == {1} or diffs == {-1}:
            found.append((i, chunk))
    return found


def score(rows, run_length=4):
    if not rows:
        return Counter()
    stage = rows[0].stage
    named = {v: k for k, v in _named_rows(stage).items()}
    tally = Counter()
    for row in rows:
        text = str(row)
        if text in named:
            tally[named[text]] += 1
        for pos, chunk in runs_in(text, run_length):
            if pos == 0:
                tally[f"front {run_length}-runs"] += 1
            elif pos + run_length == stage:
                tally[f"back {run_length}-runs"] += 1
    return tally
