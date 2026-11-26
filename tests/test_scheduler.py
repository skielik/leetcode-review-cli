from datetime import date

from lcr.scheduler import apply_grade
from lcr.models import Problem


def test_apply_grade_first_success_sets_interval_to_one():
    p = Problem(1, "Test_Problem", ["Test_Pattern"])

    apply_grade(p, 4, date(2026, 11, 24))

    assert p.repetitions == 1
    assert p.interval == 1
    assert p.ease_factor == 2.5
    assert p.next_review == date(2026, 11, 25)