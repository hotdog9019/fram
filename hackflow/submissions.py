from __future__ import annotations

from typing import Any

from .teams import Hackathon, Team, ensure_hackathon, ensure_team, get_value
from .utils import parse_datetime


class Submission:
    """Submitted hackathon project linked to a team."""

    def __init__(
        self,
        team: Team,
        project_name: str,
        submitted_at: str,
        scores: dict[str, float],
    ) -> None:
        if not project_name.strip():
            raise ValueError("Название проекта не может быть пустым")
        if not scores:
            raise ValueError("Набор оценок не может быть пустым")

        self.team = team
        self.project_name = project_name
        self.submitted_at = submitted_at
        self.scores = {criterion: float(score) for criterion, score in scores.items()}

    @property
    def team_id(self) -> int:
        """Return identifier of the linked team."""
        return self.team.id

    @classmethod
    def from_data(cls, data: dict[str, Any], teams: list[Team]) -> "Submission":
        """Create a Submission object and link it to a Team object."""
        team_id = int(data["team_id"])
        team = find_team_object_by_id(teams, team_id)
        if team is None:
            raise ValueError(f"Команда для проекта не найдена: {team_id}")
        return cls(
            team=team,
            project_name=str(data["project_name"]),
            submitted_at=str(data["submitted_at"]),
            scores=dict(data["scores"]),
        )

    def to_data(self) -> dict[str, Any]:
        """Convert a Submission object to JSON-compatible data."""
        return {
            "team_id": self.team.id,
            "project_name": self.project_name,
            "submitted_at": self.submitted_at,
            "scores": dict(self.scores),
        }

    def calculate_total_score(self) -> float:
        """Calculate total jury score."""
        return calculate_total_score(self.scores)

    def calculate_average_score(self) -> float:
        """Calculate average jury score."""
        return calculate_average_score(self.scores)

    def get_status(self, hackathon: Hackathon) -> str:
        """Return project submission status relative to the deadline."""
        return get_submission_status(self, hackathon)

    def get_jury_decision(self, passing_score: float) -> str:
        """Return preliminary jury decision."""
        return get_jury_decision(self.calculate_total_score(), passing_score)

    def __getitem__(self, key: str) -> Any:
        return self.to_data()[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self.to_data().get(key, default)

    def __str__(self) -> str:
        return f"{self.project_name} — {self.team.name}"


def find_team_object_by_id(teams: list[Team], team_id: int) -> Team | None:
    """Find Team object by identifier."""
    for team in teams:
        if team.id == team_id:
            return team
    return None


def ensure_submission(
    submission: Submission | dict[str, Any],
    teams: list[Team] | None = None,
) -> Submission:
    """Return Submission object for both object and dictionary input."""
    if isinstance(submission, Submission):
        return submission
    if teams is None:
        team = Team(
            team_id=int(submission["team_id"]),
            name=f"Team #{submission['team_id']}",
            participants=["unknown"],
        )
        return Submission(
            team=team,
            project_name=str(submission.get("project_name", "")),
            submitted_at=str(submission["submitted_at"]),
            scores=dict(submission["scores"]),
        )
    return Submission.from_data(submission, teams)


def create_submission(
    hackathon: Hackathon | dict[str, Any],
    team: Team | dict[str, Any],
    project_name: str,
    submitted_at: str,
    scores: dict[str, float],
) -> Submission:
    """Create a project submission after checking team membership."""
    team_object = ensure_team(team)
    hackathon_object = ensure_hackathon(hackathon)

    if hackathon_object.teams:
        attached_team = hackathon_object.find_team_by_id(team_object.id)
        if attached_team is None:
            raise ValueError("Команда не зарегистрирована на хакатон")
        team_object = attached_team
    if not team_object.is_registered():
        raise ValueError("Проект может сдавать только зарегистрированная команда")

    return Submission(team_object, project_name, submitted_at, scores)


def calculate_total_score(scores: dict[str, float]) -> float:
    """Calculate total jury score."""
    return sum(scores.values())


def calculate_average_score(scores: dict[str, float]) -> float:
    """Calculate average jury score."""
    if not scores:
        raise ValueError("Набор оценок не может быть пустым")
    return calculate_total_score(scores) / len(scores)


def get_submission_status(
    submission: Submission | dict[str, Any],
    hackathon: Hackathon | dict[str, Any],
) -> str:
    """Return project submission status relative to the deadline."""
    submitted_at = parse_datetime(str(get_value(submission, "submitted_at")))
    deadline = parse_datetime(str(get_value(hackathon, "submission_deadline")))
    if submitted_at <= deadline:
        return "Проект сдан вовремя"
    return "Проект сдан после дедлайна"


def get_jury_decision(total_score: float, passing_score: float) -> str:
    """Return preliminary jury decision."""
    if total_score >= passing_score:
        return f"Проект проходит в финал, итоговый балл: {total_score:.1f}"
    return f"Проект требует доработки, итоговый балл: {total_score:.1f}"


def find_submission_by_team_id(
    submissions: list[Submission | dict[str, Any]],
    team_id: int,
) -> Submission | dict[str, Any] | None:
    """Find a project submission by team identifier."""
    for submission in submissions:
        if int(get_value(submission, "team_id")) == team_id:
            return submission
    return None


def sort_projects_by_score(
    submissions: list[Submission | dict[str, Any]],
) -> list[Submission | dict[str, Any]]:
    """Return project submissions sorted by total score."""
    return sorted(
        submissions,
        key=lambda submission: calculate_total_score(get_value(submission, "scores")),
        reverse=True,
    )


def get_finalist_submissions(
    submissions: list[Submission | dict[str, Any]],
    hackathon: Hackathon | dict[str, Any],
) -> list[Submission | dict[str, Any]]:
    """Return submissions that passed the finalist score threshold."""
    passing_score = float(get_value(hackathon, "passing_score"))
    return [
        submission
        for submission in submissions
        if calculate_total_score(get_value(submission, "scores")) >= passing_score
    ]
