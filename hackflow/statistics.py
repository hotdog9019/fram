from typing import Any

from .submissions import Submission, calculate_total_score, get_finalist_submissions
from .teams import Hackathon, Team, count_registered_teams, get_value


def build_hackathon_statistics(
    hackathon: Hackathon | dict[str, Any],
    teams: list[Team | dict[str, Any]],
    submissions: list[Submission | dict[str, Any]],
) -> dict[str, float | int]:
    """Build summary statistics for a hackathon."""
    cancelled_count = 0
    participant_count = 0
    score_sum = 0.0

    for team in teams:
        if get_value(team, "status") == "cancelled":
            cancelled_count += 1
        if get_value(team, "status") == "registered":
            participant_count += len(get_value(team, "participants"))

    for submission in submissions:
        score_sum += calculate_total_score(get_value(submission, "scores"))

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
