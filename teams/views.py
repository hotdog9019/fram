from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from hackflow.teams import find_team_by_id, sort_teams_by_name
from homepage.views import load_project_data


def teams(request: HttpRequest) -> HttpResponse:
    """Show all hackathon teams."""
    hackathon, teams_list, submissions = load_project_data()
    context = {
        "hackathon": hackathon,
        "teams": sort_teams_by_name(teams_list),
        "submissions": submissions,
    }
    return render(request, "teams/team_list.html", context)


def team_detail(request: HttpRequest, team_id: int) -> HttpResponse:
    """Show a single team by id."""
    hackathon, teams_list, submissions = load_project_data()
    team = find_team_by_id(teams_list, team_id)
    submission = None
    participation_fee = None
    if team is not None:
        participation_fee = team.calculate_participation_fee(hackathon)
        for item in submissions:
            if item.team_id == team.id:
                submission = item
                break

    context = {
        "hackathon": hackathon,
        "team": team,
        "submission": submission,
        "participation_fee": participation_fee,
    }
    status = 404 if team is None else 200
    return render(request, "teams/team_detail.html", context, status=status)
