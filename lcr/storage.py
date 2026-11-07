import json
from dataclasses import asdict
from pathlib import Path
from lcr.models import Problem


DATA_PATH = Path.home() / ".lcr" / "problems.json"


def save(problems: dict[int, Problem], path: Path = DATA_PATH)  -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Problems to dict
    problems_list = []
    for problem in problems.values():
        d = asdict(problem)
        d['next_review'] = d['next_review'].isoformat()
        problems_list.append(d)
    # Save to json
    with open(path, "w") as f:
        json.dump(problems_list, f, indent=2)




