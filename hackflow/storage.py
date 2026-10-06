import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from .submissions import Submission
from .teams import Hackathon, Team


def load_json(path: str | Path) -> Any:
    """Load JSON data from a file."""
    data_path = Path(path)
    try:
        with data_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Файл данных не найден: {data_path}") from error
    except JSONDecodeError as error:
        raise ValueError(f"Файл содержит некорректный JSON: {data_path}") from error


def save_json(path: str | Path, data: Any) -> None:
    """Save JSON data to a file."""
    data_path = Path(path)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    with data_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")


def load_teams(path: str | Path) -> list[Team]:
    """Load teams from JSON and convert them to objects."""
    return [Team.from_data(item) for item in load_json(path)]


def save_teams(path: str | Path, teams: list[Team]) -> None:
    """Save Team objects to JSON."""
    save_json(path, [team.to_data() for team in teams])


def load_hackathon(path: str | Path, teams: list[Team]) -> Hackathon:
    """Load hackathon settings and attach team objects."""
    return Hackathon.from_data(load_json(path), teams)


def save_hackathon(path: str | Path, hackathon: Hackathon) -> None:
    """Save Hackathon object settings to JSON."""
    save_json(path, hackathon.to_data())


def load_submissions(path: str | Path, teams: list[Team]) -> list[Submission]:
    """Load submissions from JSON and link them to team objects."""
    return [Submission.from_data(item, teams) for item in load_json(path)]


def save_submissions(path: str | Path, submissions: list[Submission]) -> None:
    """Save Submission objects to JSON."""
    save_json(path, [submission.to_data() for submission in submissions])
