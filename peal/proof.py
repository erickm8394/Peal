from collections import defaultdict
from dataclasses import dataclass


@dataclass
class ProofResult:
    row_count: int
    repeats: dict

    @property
    def is_true(self):
        return not self.repeats

    def summary(self):
        if self.is_true:
            return f"{self.row_count} rows, true"
        n = sum(len(v) - 1 for v in self.repeats.values())
        return f"{self.row_count} rows, FALSE ({n} repeated rows)"


def prove(rows):
    seen = defaultdict(list)
    for i, row in enumerate(rows):
        seen[row].append(i)
    repeats = {row: idx for row, idx in seen.items() if len(idx) > 1}
    return ProofResult(len(rows), repeats)
