from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from hackflow.statistics import build_hackathon_statistics
from hackflow.storage import load_hackathon, load_submissions, load_teams


def load_project_data():
    """Load HackFlow objects from JSON files."""
    teams = load_teams("data/teams.json")
    hackathon = load_hackathon("data/hackathon.json", teams)
    submissions = load_submissions("data/submissions.json", teams)
    return hackathon, teams, submissions


def index(request: HttpRequest) -> HttpResponse:
    """Show project homepage with summary statistics."""
    hackathon, teams, submissions = load_project_data()
    context = {
        "hackathon": hackathon,
        "statistics": build_hackathon_statistics(hackathon, teams, submissions),
    }
    return render(request, "homepage/index.html", context)


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Return a custom 404 page."""
    return render(request, "homepage/404.html", status=404)
