from .rows import BELL_CHARS, Row

CROSS_CHARS = "xX-"


class PlaceNotationError(ValueError):
    pass


class Change:
    __slots__ = ("stage", "places", "_perm")

    def __init__(self, stage, places):
        self.stage = stage
        self.places = frozenset(_fill_external_places(stage, places))
        self._perm = self._build_perm()

    def _build_perm(self):
        perm = list(range(self.stage))
        i = 0
        while i < self.stage:
            if i in self.places:
                i += 1
                continue
            if i + 1 >= self.stage or (i + 1) in self.places:
                raise PlaceNotationError(
                    f"bell in position {i + 1} has nowhere to go on {self.stage} bells"
                )
            perm[i], perm[i + 1] = i + 1, i
            i += 2
        return Row(perm)

    def apply(self, row):
        return row * self._perm

    def as_row(self):
        return self._perm

    def is_cross(self):
        return not self.places

    def __eq__(self, other):
        return isinstance(other, Change) and (self.stage, self.places) == (other.stage, other.places)

    def __hash__(self):
        return hash((self.stage, self.places))

    def __str__(self):
        if not self.places:
            return "x"
        return "".join(BELL_CHARS[p] for p in sorted(self.places))

    def __repr__(self):
        return f"Change({self.stage}, '{self}')"


def _fill_external_places(stage, places):
    places = set(places)
    for p in places:
        if not 0 <= p < stage:
            raise PlaceNotationError(f"place {p + 1} is outside stage {stage}")
    if not places:
        if stage % 2:
            raise PlaceNotationError(f"cross change impossible on {stage} bells")
        return places
    if min(places) % 2 == 1:
        places.add(0)
    if (stage - 1 - max(places)) % 2 == 1:
        places.add(stage - 1)
    return places


def _tokens(segment):
    current = []
    for ch in segment:
        if ch in CROSS_CHARS:
            if current:
                yield current
                current = []
            yield []
        elif ch == ".":
            if current:
                yield current
            current = []
        elif ch.isspace():
            continue
        else:
            try:
                current.append(BELL_CHARS.index(ch.upper()))
            except ValueError:
                raise PlaceNotationError(f"unexpected character {ch!r}") from None
    if current:
        yield current


def _palindrome(seq):
    return seq + seq[-2::-1]


def parse(text, stage):
    text = text.strip()
    if not text:
        raise PlaceNotationError("empty place notation")

    out = []
    if text[0] in "&+":
        for segment in _split_prefixed(text):
            mode, body = segment[0], segment[1:]
            changes = [Change(stage, t) for t in _tokens(body)]
            out.extend(_palindrome(changes) if mode == "&" else changes)
    elif "," in text:
        for segment in text.split(","):
            changes = [Change(stage, t) for t in _tokens(segment)]
            if not changes:
                raise PlaceNotationError(f"empty segment in {text!r}")
            out.extend(_palindrome(changes))
    else:
        out = [Change(stage, t) for t in _tokens(text)]

    if not out:
        raise PlaceNotationError(f"no changes in {text!r}")
    return out


def _split_prefixed(text):
    parts = []
    for raw in text.split(","):
        raw = raw.strip()
        if not raw:
            continue
        if raw[0] not in "&+":
            raw = "+" + raw
        parts.append(raw)
    return parts


def to_string(changes):
    pieces = []
    for c in changes:
        s = str(c)
        if pieces and s != "x" and pieces[-1] != "x":
            pieces.append(".")
        pieces.append(s)
    return "".join(pieces)
