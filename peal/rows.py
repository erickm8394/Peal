BELL_CHARS = "1234567890ETABCDFGHJKLMNPQRSUVWYZ"
MAX_STAGE = len(BELL_CHARS)


class RowError(ValueError):
    pass


def bell_from_char(ch):
    idx = BELL_CHARS.find(ch.upper())
    if idx < 0:
        raise RowError(f"not a bell: {ch!r}")
    return idx


class Row:
    __slots__ = ("_bells",)

    def __init__(self, bells):
        bells = tuple(bells)
        if sorted(bells) != list(range(len(bells))):
            raise RowError(f"not a permutation: {bells}")
        self._bells = bells

    @classmethod
    def rounds(cls, stage):
        if not 1 <= stage <= MAX_STAGE:
            raise RowError(f"unsupported stage {stage}")
        return cls(range(stage))

    @classmethod
    def parse(cls, text):
        return cls(bell_from_char(c) for c in text.strip())

    @property
    def stage(self):
        return len(self._bells)

    def is_rounds(self):
        return all(b == i for i, b in enumerate(self._bells))

    def position_of(self, bell):
        return self._bells.index(bell)

    def inverse(self):
        out = [0] * self.stage
        for pos, bell in enumerate(self._bells):
            out[bell] = pos
        return Row(out)

    def __mul__(self, other):
        if not isinstance(other, Row):
            return NotImplemented
        if other.stage != self.stage:
            raise RowError("stage mismatch")
        return Row(self._bells[i] for i in other._bells)

    def __getitem__(self, i):
        return self._bells[i]

    def __iter__(self):
        return iter(self._bells)

    def __len__(self):
        return len(self._bells)

    def __eq__(self, other):
        return isinstance(other, Row) and self._bells == other._bells

    def __hash__(self):
        return hash(self._bells)

    def __str__(self):
        return "".join(BELL_CHARS[b] for b in self._bells)

    def __repr__(self):
        return f"Row('{self}')"
