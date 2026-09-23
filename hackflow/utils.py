from datetime import datetime
from typing import Any


DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def parse_datetime(value: str) -> datetime:
    """Convert a project datetime string to datetime."""
    try:
        return datetime.strptime(value, DATETIME_FORMAT)
    except ValueError as error:
        message = f"Дата должна соответствовать формату {DATETIME_FORMAT}: {value}"
        raise ValueError(message) from error


def format_datetime(value: datetime) -> str:
    """Convert datetime to the project string format."""
    return value.strftime("%d.%m.%Y %H:%M")


def get_next_id(items: list[dict[str, Any]]) -> int:
    """Return next numeric identifier for a list of dictionaries."""
    identifiers = [int(item.get("id", 0)) for item in items]
    return max(identifiers, default=0) + 1
