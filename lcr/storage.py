import json
from dataclasses import asdict
from pathlib import Path
from lcr.models import Problem


DATA_PATH = Path.home() / ".lcr" / "problems.json"


def _to_dict(problem: Problem) -> dict:
    d = asdict(problem)
    d['next_review'] = d['next_review'].isoformat()
    return d


def save(problems: dict[int, Problem], path: Path = DATA_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump([_to_dict(p) for p in problems.values()], f, indent=2)




