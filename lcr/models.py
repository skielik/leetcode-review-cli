from dataclasses import dataclass, field
from datetime import date


@dataclass
class Problem:
    number: int
    title: str
    patterns: list[str]
    repetitions: int = 0
    interval: int = 0
    ease_factor: float = 2.5
    next_review: date = field(default_factory=date.today)


