import json
from dataclasses import asdict
from pathlib import Path
from datetime import date

from lcr.models import Problem


DATA_PATH = Path.home() / ".lcr" / "problems.json"


def _to_dict(problem: Problem) -> dict:
    d = asdict(problem)
    d['next_review'] = d['next_review'].isoformat()
    return d


def _from_dict(data: dict) -> Problem:
    data = dict(data)
    data['next_review'] = date.fromisoformat(data['next_review'])
    problem = Problem(**data)
    return problem


def save(problems: dict[int, Problem], path: Path = DATA_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump([_to_dict(p) for p in problems.values()], f, indent=2)


def load(path: Path = DATA_PATH) -> dict[int, Problem]:
    if not path.exists():
        return {}
    with open(path, "r") as f:
        list_with_data = json.load(f)
    problems = {element['number']: _from_dict(element) for element in list_with_data}
    return problems
