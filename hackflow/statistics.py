from typing import Any

from .submissions import calculate_total_score, get_finalist_submissions
from .teams import count_registered_teams


def build_hackathon_statistics(
    hackathon: dict[str, Any],
    teams: list[dict[str, Any]],
    submissions: list[dict[str, Any]],
) -> dict[str, float | int]:
    """Build summary statistics for a hackathon."""
    cancelled_count = 0
    participant_count = 0
    score_sum = 0.0

    for team in teams:
        if team.get("status") == "cancelled":
            cancelled_count += 1
        if team.get("status") == "registered":
            participant_count += len(team["participants"])

    for submission in submissions:
        score_sum += calculate_total_score(submission["scores"])

    average_project_score = 0.0
    if submissions:
        average_project_score = score_sum / len(submissions)

    finalists = get_finalist_submissions(submissions, hackathon)

    return {
        "registered_teams": count_registered_teams(teams),
        "cancelled_teams": cancelled_count,
        "participants": participant_count,
        "submitted_projects": len(submissions),
        "finalists": len(finalists),
        "average_project_score": average_project_score,
    }
