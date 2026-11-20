import argparse
from datetime import date
from pathlib import Path

from lcr.models import Problem
from lcr.scheduler import MAXIMUM_GRADE, MINIMUM_GRADE, apply_grade, due_problems
from lcr.storage import DATA_PATH, load, save


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="lcr",
        description="LeetCode Review. Spaced repetition of solved LeetCode problems.",
    )
    parser.add_argument(
        "--data-file",
        type=Path,
        default=DATA_PATH,
        help="Path to the JSON file with problems.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_cmd = subparsers.add_parser("add", help="Add a new problem.")
    add_cmd.add_argument("number", type=int, help="The number of the problem.")
    add_cmd.add_argument("title", help="The name/title of the problem.")
    add_cmd.add_argument(
        "--patterns",
        nargs="+",
        required=True,
        help="One or more patterns used to solve the problem.",
    )
    add_cmd.add_argument(
        "--grade",
        type=int,
        required=True,
        choices=range(MINIMUM_GRADE, MAXIMUM_GRADE + 1),
        help=f"Recall quality from {MINIMUM_GRADE} (forgot) to {MAXIMUM_GRADE} (perfect).",
    )

    subparsers.add_parser("today", help="Show problems to solve today.")

    args = parser.parse_args(argv)

    if args.command == "add":
        _cmd_add(args, add_cmd)
    elif args.command == "today":
        _cmd_today(args)


def _cmd_add(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    problems = load(args.data_file)
    if args.number in problems:
        parser.error(
            f"problem {args.number} already exists; "
            f"use 'lcr review {args.number}' to review it"
        )
    new_problem = Problem(args.number, args.title, args.patterns)
    apply_grade(new_problem, args.grade, date.today())
    problems[new_problem.number] = new_problem
    save(problems, args.data_file)
    print(
        f"Added {new_problem.number} {new_problem.title}. "
        f"Next review: {new_problem.next_review}."
    )


def _cmd_today(args: argparse.Namespace) -> None:
    problems = load(args.data_file)
    today = date.today()
    if not problems:
        print("No problems yet. Add one with 'lcr add'.")
        return
    due = due_problems(problems, today)
    if not due:
        print("No problems due today.")
        return
    number_width = len("#")
    title_width = len("Title")
    overdue_width = len("Days overdue")
    for problem in due:
        number_width = max(number_width, len(str(problem.number)))
        title_width = max(title_width, len(problem.title))
        overdue_width = max(overdue_width, len(str((today - problem.next_review).days)))
    print(f"|{"#":<{number_width}}|{"Title":<{title_width}}|{"Days overdue":>{overdue_width}}|")
    for problem in due:
        days_overdue = (today - problem.next_review).days
        print(f"|{problem.number:<{number_width}}|{problem.title:<{title_width}}|{days_overdue:>{overdue_width}}|")
        