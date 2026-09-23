from typing import Any

from .utils import get_next_id


def count_registered_teams(teams: list[dict[str, Any]]) -> int:
    """Count teams with active registration."""
    registered_count = 0
    for team in teams:
        if team.get("status") == "registered":
            registered_count += 1
    return registered_count


def is_registration_available(
    hackathon: dict[str, Any],
    teams: list[dict[str, Any]],
) -> bool:
    """Check whether a new team can be registered."""
    if not bool(hackathon.get("registration_is_open")):
        return False
    return count_registered_teams(teams) < int(hackathon["max_teams"])


def find_team_by_id(
    teams: list[dict[str, Any]],
    team_id: int,
) -> dict[str, Any] | None:
    """Find a team by identifier."""
    for team in teams:
        if int(team["id"]) == team_id:
            return team
    return None


def find_teams_by_name(
    teams: list[dict[str, Any]],
    query: str,
) -> list[dict[str, Any]]:
    """Find teams whose names contain the query."""
    query_lower = query.lower()
    result = []
    for team in teams:
        if query_lower in str(team["name"]).lower():
            result.append(team)
    return result


def sort_teams_by_name(teams: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return teams sorted by name."""
    return sorted(teams, key=lambda team: str(team["name"]).lower())


def add_team_registration(
    hackathon: dict[str, Any],
    teams: list[dict[str, Any]],
    name: str,
    participants: list[str],
    has_student_discount: bool,
) -> dict[str, Any]:
    """Add a new team registration."""
    if not is_registration_available(hackathon, teams):
        raise ValueError("Регистрация команды недоступна")
    if not name.strip():
        raise ValueError("Название команды не может быть пустым")
    if not participants:
        raise ValueError("В команде должен быть хотя бы один участник")
    for team in teams:
        same_name = str(team["name"]).lower() == name.lower()
        if same_name and team.get("status") == "registered":
            raise ValueError("Команда с таким названием уже зарегистрирована")

    team = {
        "id": get_next_id(teams),
        "name": name,
        "participants": participants,
        "status": "registered",
        "has_student_discount": has_student_discount,
    }
    teams.append(team)
    return team


def cancel_team_registration(
    teams: list[dict[str, Any]],
    team_id: int,
) -> dict[str, Any]:
    """Cancel an existing team registration."""
    team = find_team_by_id(teams, team_id)
    if team is None:
        raise ValueError("Команда не найдена")
    if team.get("status") == "cancelled":
        raise ValueError("Регистрация команды уже отменена")
    team["status"] = "cancelled"
    return team


def calculate_participation_fee(
    team: dict[str, Any],
    hackathon: dict[str, Any],
) -> float:
    """Calculate participation fee for a team."""
    fee_per_participant = float(hackathon["fee_per_participant"])
    total_fee = len(team["participants"]) * fee_per_participant
    if bool(team.get("has_student_discount")):
        discount = float(hackathon.get("student_discount_percent", 0))
        return total_fee * (100 - discount) / 100
    return total_fee
