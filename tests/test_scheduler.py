from datetime import date

import pytest

from lcr.scheduler import apply_grade, due_problems
from lcr.models import Problem


TODAY = date(2026, 11, 1)


def test_apply_grade_first_success():
    p = Problem(1, "Test_Problem", ["Test_Pattern"])

    apply_grade(p, 4, TODAY)

    assert p.repetitions == 1
    assert p.interval == 1
    assert p.ease_factor == 2.5
    assert p.next_review == date(2026, 11, 2)


def test_apply_grade_second_success():
    p = Problem(1, "Test_Problem", ["Test_Pattern"], repetitions=1, interval=1)

    apply_grade(p, 4, TODAY)

    assert p.repetitions == 2
    assert p.interval == 6
    assert p.ease_factor == 2.5
    assert p.next_review == date(2026, 11, 7)


def test_apply_grade_third_success():
    p = Problem(1, "Test_Problem", ["Test_Pattern"], repetitions=2, interval=6, ease_factor=2.6)

    apply_grade(p, 3, TODAY)

    assert p.repetitions == 3
    assert p.interval == 16
    assert p.ease_factor == pytest.approx(2.46)
    assert p.next_review == date(2026, 11, 17)


def test_apply_grade_failure_after_success():
    p = Problem(1, "Test_Problem", ["Test_Pattern"], repetitions=3, interval=16, ease_factor=2.46)

    apply_grade(p, 2, TODAY)

    assert p.repetitions == 0
    assert p.interval == 1
    assert p.ease_factor == pytest.approx(2.14)
    assert p.next_review == date(2026, 11, 2)


@pytest.mark.parametrize(
    "grade, expected",
    [
        (0, 1.7),
        (1, 1.96),
        (2, 2.18),
        (3, 2.36),
        (4, 2.5),
        (5, 2.6)
    ]
)
def test_apply_grade_changes_ease_factor_by_grade(grade, expected):
    p = Problem(1, "Test_Problem", ["Test_Pattern"])

    apply_grade(p, grade, TODAY)

    assert p.ease_factor == pytest.approx(expected)


def test_apply_grade_minimum_ease_factor_and_grade_zero():
    p = Problem(1, "Test_Problem", ["Test_Pattern"], ease_factor=1.5)

    apply_grade(p, 0, TODAY)

    assert p.ease_factor == pytest.approx(1.3)


@pytest.mark.parametrize("grade", [6, -1])
def test_apply_grade_invalid_grade_raises_value_error(grade):
    p = Problem(1, "Test_Problem", ["Test_Pattern"])

    with pytest.raises(ValueError):
        apply_grade(p, grade, TODAY)


@pytest.mark.parametrize("grade", [6, -1])
def test_apply_grade_invalid_grade_leaves_problem_unchanged(grade):
    p = Problem(
        1,
        "Test_Problem", 
        ["Test_Pattern"], 
        repetitions=2, 
        interval=15, 
        ease_factor=2.6, 
        next_review=date(2026,11, 5)
    )
    p_duplicate = Problem(
        1,
        "Test_Problem",
        ["Test_Pattern"], 
        repetitions=2, 
        interval=15, 
        ease_factor=2.6, 
        next_review=date(2026,11, 5)
    )

    with pytest.raises(ValueError):
        apply_grade(p, grade, TODAY)

    assert p == p_duplicate


def test_due_problems_excludes_future_problem():
    p_1 = Problem(1, "Test_Problem_1", ["Test_Pattern"], next_review=TODAY)
    p_2 = Problem(2, "Test_Problem_2", ["Test_Pattern"], next_review=date(2026, 10, 1))
    p_3 = Problem(3, "Test_Problem_3", ["Test_Pattern"], next_review=date(2026, 12, 1))
    problems = {1: p_1, 2: p_2, 3: p_3}

    assert due_problems(problems, TODAY) == [p_2, p_1]


def test_due_problems_sorts_by_date_then_ease():
    p_1 = Problem(1, "Test_Problem_1", ["Test_Pattern"], next_review=TODAY, ease_factor=1.8)
    p_2 = Problem(2, "Test_Problem_2", ["Test_Pattern"], next_review=TODAY, ease_factor= 2.6)
    p_3 = Problem(3, "Test_Problem_3", ["Test_Pattern"], next_review=date(2026, 10, 1), ease_factor=2.5)
    p_4 = Problem(4, "Test_Problem_4", ["Test_Pattern"], next_review=date(2026, 10, 1), ease_factor=1.4)
    problems = {1: p_1, 2: p_2, 3: p_3, 4: p_4}

    assert due_problems(problems, TODAY) == [p_4, p_3, p_1, p_2]


def test_due_problems_empty_dict():
    problems = {}

    assert due_problems(problems, TODAY) == []