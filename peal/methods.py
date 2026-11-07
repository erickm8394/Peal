from dataclasses import dataclass, field

from . import notation
from .rows import Row

STAGE_NAMES = {
    3: "Singles",
    4: "Minimus",
    5: "Doubles",
    6: "Minor",
    7: "Triples",
    8: "Major",
    9: "Caters",
    10: "Royal",
    11: "Cinques",
    12: "Maximus",
}


@dataclass(frozen=True)
class Method:
    name: str
    stage: int
    place_notation: str
    changes: tuple = field(init=False, repr=False, compare=False)

    def __post_init__(self):
        object.__setattr__(
            self, "changes", tuple(notation.parse(self.place_notation, self.stage))
        )

    @property
    def title(self):
        return f"{self.name} {STAGE_NAMES.get(self.stage, str(self.stage))}"

    @property
    def lead_length(self):
        return len(self.changes)

    def lead(self, start=None):
        row = start or Row.rounds(self.stage)
        rows = [row]
        for change in self.changes[:-1]:
            row = change.apply(row)
            rows.append(row)
        return rows

    def lead_head(self, start=None):
        row = start or Row.rounds(self.stage)
        for change in self.changes:
            row = change.apply(row)
        return row

    def lead_head_perm(self):
        return self.lead_head()

    def hunt_bells(self):
        lh = self.lead_head_perm()
        return [b for b in range(self.stage) if lh[b] == b]

    def plain_course(self):
        rows = []
        row = Row.rounds(self.stage)
        while True:
            rows.extend(self.lead(row))
            row = self.lead_head(row)
            if row.is_rounds():
                return rows
            if len(rows) > 50_000:
                raise RuntimeError(f"{self.title} never comes round")

    def leads_in_course(self):
        return len(self.plain_course()) // self.lead_length


LIBRARY = [
    Method("Plain Bob", 5, "&5.1.5.1.5,+125"),
    Method("Plain Bob", 6, "x16x16x16,12"),
    Method("Plain Bob", 7, "&7.1.7.1.7.1.7,+127"),
    Method("Plain Bob", 8, "x18x18x18x18,12"),
    Method("Little Bob", 6, "x16x14,12"),
    Method("Cambridge Surprise", 6, "x36x14x12x36x14x56,12"),
    Method("Cambridge Surprise", 8, "x38x14x1258x36x14x58x16x78,12"),
    Method("Yorkshire Surprise", 8, "x38x14x58x16x12x38x14x78,12"),
]


def find_method(title):
    wanted = " ".join(title.lower().split())
    for m in LIBRARY:
        if m.title.lower() == wanted:
            return m
    raise KeyError(f"unknown method: {title}")
