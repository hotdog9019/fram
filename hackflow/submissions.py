from typing import Any

from .utils import parse_datetime


def calculate_total_score(scores: dict[str, float]) -> float:
    """Calculate total jury score."""
    return sum(scores.values())


def calculate_average_score(scores: dict[str, float]) -> float:
    """Calculate average jury score."""
    if not scores:
        raise ValueError("Набор оценок не может быть пустым")
    return calculate_total_score(scores) / len(scores)


def get_submission_status(
    submission: dict[str, Any],
    hackathon: dict[str, Any],
) -> str:
    """Return project submission status relative to the deadline."""
    submitted_at = parse_datetime(str(submission["submitted_at"]))
    deadline = parse_datetime(str(hackathon["submission_deadline"]))
    if submitted_at <= deadline:
        return "Проект сдан вовремя"
    return "Проект сдан после дедлайна"


def get_jury_decision(total_score: float, passing_score: float) -> str:
    """Return preliminary jury decision."""
    if total_score >= passing_score:
        return f"Проект проходит в финал, итоговый балл: {total_score:.1f}"
    return f"Проект требует доработки, итоговый балл: {total_score:.1f}"


def find_submission_by_team_id(
    submissions: list[dict[str, Any]],
    team_id: int,
) -> dict[str, Any] | None:
    """Find a project submission by team identifier."""
    for submission in submissions:
        if int(submission["team_id"]) == team_id:
            return submission
    return None


def sort_projects_by_score(
    submissions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return project submissions sorted by total score."""
    return sorted(
        submissions,
        key=lambda submission: calculate_total_score(submission["scores"]),
        reverse=True,
    )


def get_finalist_submissions(
    submissions: list[dict[str, Any]],
    hackathon: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return submissions that passed the finalist score threshold."""
    finalists = []
    passing_score = float(hackathon["passing_score"])
    for submission in submissions:
        total_score = calculate_total_score(submission["scores"])
        if total_score >= passing_score:
            finalists.append(submission)
    return finalists
