from datetime import date, timedelta

from lcr.models import Problem


MAXIMUM_GRADE = 5
MINIMUM_GRADE = 0
PASSING_GRADE = 3
MINIMUM_EASE_FACTOR = 1.3


def apply_grade(problem: Problem, grade: int, today: date) -> None:
    """Update the problem's review schedule using the SM-2 algorithm.
    
    Modifies the problem in place: repetitions, interval, ease_factor
    and next_review are recalculated from the grade. Returns None.

    Args:
        problem: The problem that was just reviewed.
        grade: Self-assessed recall quality from 0 to 5.
            Grades below 3 count as a failed review.
        today: The review date; the next review is scheduled from it.

    Raises:
        ValueError: If grade is outside the range 0-5.
    """
    if grade < MINIMUM_GRADE or grade > MAXIMUM_GRADE:
        raise ValueError(f"grade must be between {MINIMUM_GRADE} and {MAXIMUM_GRADE}, got {grade}")
    if grade >= PASSING_GRADE:
        if problem.repetitions == 0: 
            problem.interval = 1
        elif problem.repetitions == 1: 
            problem.interval = 6
        else: 
            problem.interval = round(problem.interval * problem.ease_factor)
        problem.repetitions += 1
    else:
        problem.repetitions = 0
        problem.interval = 1
    # SM-2 ease factor formula
    problem.ease_factor += (0.1 - (MAXIMUM_GRADE - grade) * (0.08 + (MAXIMUM_GRADE - grade) * 0.02))
    problem.ease_factor = max(MINIMUM_EASE_FACTOR, problem.ease_factor)
    problem.next_review = today + timedelta(days=problem.interval)
