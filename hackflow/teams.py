from __future__ import annotations

from typing import Any

from .utils import get_next_id


class Team:
    """Hackathon team with registration state and participants."""

    def __init__(
        self,
        team_id: int,
        name: str,
        participants: list[str],
        status: str = "registered",
        has_student_discount: bool = False,
    ) -> None:
        if not name.strip():
            raise ValueError("Название команды не может быть пустым")
        if not participants:
            raise ValueError("В команде должен быть хотя бы один участник")

        self.id = int(team_id)
        self.name = name
        self.participants = list(participants)
        self.status = status
        self.has_student_discount = bool(has_student_discount)

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Team":
        """Create a Team object from JSON-compatible data."""
        return cls(
            team_id=int(data["id"]),
            name=str(data["name"]),
            participants=list(data["participants"]),
            status=str(data.get("status", "registered")),
            has_student_discount=bool(data.get("has_student_discount", False)),
        )

    def to_data(self) -> dict[str, Any]:
        """Convert a Team object to JSON-compatible data."""
        return {
            "id": self.id,
            "name": self.name,
            "participants": list(self.participants),
            "status": self.status,
            "has_student_discount": self.has_student_discount,
        }

    def cancel_registration(self) -> None:
        """Cancel team registration."""
        if self.status == "cancelled":
            raise ValueError("Регистрация команды уже отменена")
        self.status = "cancelled"

    def is_registered(self) -> bool:
        """Return whether the team has active registration."""
        return self.status == "registered"

    def calculate_participation_fee(self, hackathon: Any) -> float:
        """Calculate participation fee using hackathon settings."""
        fee_per_participant = float(get_value(hackathon, "fee_per_participant"))
        total_fee = len(self.participants) * fee_per_participant
        if self.has_student_discount:
            discount = float(get_value(hackathon, "student_discount_percent", 0))
            return total_fee * (100 - discount) / 100
        return total_fee

    def __getitem__(self, key: str) -> Any:
        return self.to_data()[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.to_data().get(key, default)

    def __str__(self) -> str:
        return f"{self.name} ({len(self.participants)} участн., {self.status})"


class Hackathon:
    """Hackathon aggregate that owns team registration rules."""

    def __init__(
        self,
        hackathon_id: int,
        name: str,
        max_teams: int,
        registration_is_open: bool,
        fee_per_participant: float,
        student_discount_percent: float,
        submission_deadline: str,
        passing_score: float,
        teams: list[Team] | None = None,
    ) -> None:
        self.id = int(hackathon_id)
        self.name = name
        self.max_teams = int(max_teams)
        self.registration_is_open = bool(registration_is_open)
        self.fee_per_participant = float(fee_per_participant)
        self.student_discount_percent = float(student_discount_percent)
        self.submission_deadline = submission_deadline
        self.passing_score = float(passing_score)
        self.teams = list(teams or [])

    @classmethod
    def from_data(
        cls,
        data: dict[str, Any],
        teams: list[Team] | None = None,
    ) -> "Hackathon":
        """Create a Hackathon object from JSON-compatible data."""
        return cls(
            hackathon_id=int(data["id"]),
            name=str(data["name"]),
            max_teams=int(data["max_teams"]),
            registration_is_open=bool(data["registration_is_open"]),
            fee_per_participant=float(data["fee_per_participant"]),
            student_discount_percent=float(data.get("student_discount_percent", 0)),
            submission_deadline=str(data["submission_deadline"]),
            passing_score=float(data["passing_score"]),
            teams=teams,
        )

    def to_data(self) -> dict[str, Any]:
        """Convert a Hackathon object to JSON-compatible data."""
        return {
            "id": self.id,
            "name": self.name,
            "max_teams": self.max_teams,
            "registration_is_open": self.registration_is_open,
            "fee_per_participant": self.fee_per_participant,
            "student_discount_percent": self.student_discount_percent,
            "submission_deadline": self.submission_deadline,
            "passing_score": self.passing_score,
        }

    def add_team(self, team: Team) -> None:
        """Attach a team to the hackathon after validation."""
        if not self.is_registration_available():
            raise ValueError("Регистрация команды недоступна")
        if self.find_team_by_name(team.name) is not None:
            raise ValueError("Команда с таким названием уже зарегистрирована")
        self.teams.append(team)

    def create_team(
        self,
        name: str,
        participants: list[str],
        has_student_discount: bool,
    ) -> Team:
        """Create and register a new team."""
        team = Team(
            team_id=get_next_id(self.teams),
            name=name,
            participants=participants,
            has_student_discount=has_student_discount,
        )
        self.add_team(team)
        return team

    def find_team_by_id(self, team_id: int) -> Team | None:
        """Find attached team by identifier."""
        return find_team_by_id(self.teams, team_id)

    def find_team_by_name(self, name: str) -> Team | None:
        """Find registered attached team by exact name."""
        name_lower = name.lower()
        for team in self.teams:
            if team.name.lower() == name_lower and team.is_registered():
                return team
        return None

    def count_registered_teams(self) -> int:
        """Count attached teams with active registration."""
        return count_registered_teams(self.teams)

    def is_registration_available(self) -> bool:
        """Return whether a new team can be registered."""
        return (
            self.registration_is_open
            and self.count_registered_teams() < self.max_teams
        )

    def __getitem__(self, key: str) -> Any:
        return self.to_data()[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.to_data().get(key, default)

    def __str__(self) -> str:
        return f"{self.name}: {self.count_registered_teams()}/{self.max_teams} команд"


def get_value(source: Any, key: str, default: Any = None) -> Any:
    """Read a field from an object or dictionary."""
    if isinstance(source, dict):
        return source.get(key, default)
    return getattr(source, key, default)


def ensure_team(team: Team | dict[str, Any]) -> Team:
    """Return Team object for both object and dictionary input."""
    if isinstance(team, Team):
        return team
    return Team.from_data(team)


def ensure_hackathon(
    hackathon: Hackathon | dict[str, Any],
    teams: list[Team | dict[str, Any]] | None = None,
) -> Hackathon:
    """Return Hackathon object for both object and dictionary input."""
    converted_teams = None
    if teams is not None:
        converted_teams = [ensure_team(team) for team in teams]
    if isinstance(hackathon, Hackathon):
        if converted_teams is not None:
            hackathon.teams = converted_teams
        return hackathon
    return Hackathon.from_data(hackathon, converted_teams)


def count_registered_teams(teams: list[Team | dict[str, Any]]) -> int:
    """Count teams with active registration."""
    return sum(1 for team in teams if get_value(team, "status") == "registered")


def is_registration_available(
    hackathon: Hackathon | dict[str, Any],
    teams: list[Team | dict[str, Any]],
) -> bool:
    """Check whether a new team can be registered."""
    if not bool(get_value(hackathon, "registration_is_open")):
        return False
    return count_registered_teams(teams) < int(get_value(hackathon, "max_teams"))


def find_team_by_id(
    teams: list[Team | dict[str, Any]],
    team_id: int,
) -> Team | dict[str, Any] | None:
    """Find a team by identifier."""
    for team in teams:
        if int(get_value(team, "id")) == team_id:
            return team
    return None


def find_teams_by_name(
    teams: list[Team | dict[str, Any]],
    query: str,
) -> list[Team | dict[str, Any]]:
    """Find teams whose names contain the query."""
    query_lower = query.lower()
    return [
        team
        for team in teams
        if query_lower in str(get_value(team, "name")).lower()
    ]


def sort_teams_by_name(
    teams: list[Team | dict[str, Any]],
) -> list[Team | dict[str, Any]]:
    """Return teams sorted by name."""
    return sorted(teams, key=lambda team: str(get_value(team, "name")).lower())


def add_team_registration(
    hackathon: Hackathon | dict[str, Any],
    teams: list[Team | dict[str, Any]],
    name: str,
    participants: list[str],
    has_student_discount: bool,
) -> Team | dict[str, Any]:
    """Add a new team registration."""
    if not is_registration_available(hackathon, teams):
        raise ValueError("Регистрация команды недоступна")

    new_id = get_next_id(teams)
    new_team = Team(
        new_id,
        name,
        participants,
        has_student_discount=has_student_discount,
    )
    for team in teams:
        same_name = str(get_value(team, "name")).lower() == name.lower()
        if same_name and get_value(team, "status") == "registered":
            raise ValueError("Команда с таким названием уже зарегистрирована")

    if isinstance(hackathon, Hackathon) and teams is hackathon.teams:
        hackathon.add_team(new_team)
        return new_team

    if isinstance(teams, list) and all(isinstance(team, Team) for team in teams):
        teams.append(new_team)
        return new_team

    team_data = new_team.to_data()
    teams.append(team_data)
    return team_data


def cancel_team_registration(
    teams: list[Team | dict[str, Any]],
    team_id: int,
) -> Team | dict[str, Any]:
    """Cancel an existing team registration."""
    team = find_team_by_id(teams, team_id)
    if team is None:
        raise ValueError("Команда не найдена")
    if isinstance(team, Team):
        team.cancel_registration()
    else:
        if team.get("status") == "cancelled":
            raise ValueError("Регистрация команды уже отменена")
        team["status"] = "cancelled"
    return team


def calculate_participation_fee(
    team: Team | dict[str, Any],
    hackathon: Hackathon | dict[str, Any],
) -> float:
    """Calculate participation fee for a team."""
    return ensure_team(team).calculate_participation_fee(hackathon)
