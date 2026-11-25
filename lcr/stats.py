"""Per-pattern statistics built from the problems' ease factors."""

from collections import defaultdict
from dataclasses import dataclass

from lcr.models import Problem


@dataclass
class PatternStat:
    """Aggregated review statistics for one pattern."""

    pattern: str
    count: int
    average_ease: float


def pattern_stats(problems: dict[int, Problem]) -> list[PatternStat]:
    """Return per-pattern statistics, weakest pattern first.

    A problem with several patterns counts toward each of them. The
    average ease of a pattern is the mean ease_factor of its problems;
    a lower value means the pattern is harder to recall.

    Args:
        problems: All problems, keyed by problem number.

    Returns:
        One PatternStat per pattern, sorted by average_ease ascending;
        patterns with the same average are ordered by count, largest
        first. An empty list if there are no problems.
    """
    ease_by_pattern = defaultdict(list)
    for problem in problems.values():
        for pattern in problem.patterns:
            ease_by_pattern[pattern].append(problem.ease_factor)

    stats = [
        PatternStat(pattern, len(eases), sum(eases) / len(eases))
        for pattern, eases in ease_by_pattern.items()
    ]
    return sorted(stats, key=lambda stat: (stat.average_ease, -stat.count))