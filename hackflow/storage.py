import json
from json import JSONDecodeError
from pathlib import Path
from typing import Any


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
