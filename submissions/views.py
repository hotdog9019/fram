from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from hackflow.submissions import (
    find_submission_by_team_id,
    get_jury_decision,
    get_submission_status,
    sort_projects_by_score,
)
from homepage.views import load_project_data


def submissions(request: HttpRequest) -> HttpResponse:
    """Show all project submissions."""
    hackathon, teams, submissions_list = load_project_data()
    context = {
        "hackathon": hackathon,
        "teams": teams,
        "submissions": sort_projects_by_score(submissions_list),
    }
    return render(request, "submissions/submission_list.html", context)


def submission_detail(request: HttpRequest, team_id: int) -> HttpResponse:
    """Show a project submission by team id."""
    hackathon, teams, submissions_list = load_project_data()
    submission = find_submission_by_team_id(submissions_list, team_id)
    context = {
        "hackathon": hackathon,
        "submission": submission,
        "status_text": "",
        "jury_decision": "",
    }
    if submission is not None:
        context["status_text"] = get_submission_status(submission, hackathon)
        context["jury_decision"] = get_jury_decision(
            submission.calculate_total_score(),
            hackathon.passing_score,
        )

    status = 404 if submission is None else 200
    return render(
        request,
        "submissions/submission_detail.html",
        context,
        status=status,
    )
