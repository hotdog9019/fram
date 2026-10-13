from django.http import HttpRequest, HttpResponse

from hackflow.teams import find_team_by_id, sort_teams_by_name
from homepage.views import load_project_data, page


def teams(request: HttpRequest) -> HttpResponse:
    """Show all hackathon teams."""
    hackathon, teams_list, submissions = load_project_data()
    items = ""
    for team in sort_teams_by_name(teams_list):
        badge = "bg-success" if team.is_registered() else "bg-secondary"
        status = "зарегистрирована" if team.is_registered() else "отменена"
        items += f"""
<li class="list-group-item d-flex justify-content-between align-items-center">
  <a href="/teams/{team.id}/">{team.name}</a>
  <span>
    <span class="badge {badge} me-2">{status}</span>
    {len(team.participants)} участн.
  </span>
</li>
"""

    content = f"""
<h1>Команды</h1>
<p class="text-muted">
  Хакатон: {hackathon.name}. Сданных проектов: {len(submissions)}.
</p>
<ul class="list-group">{items}</ul>
"""
    return HttpResponse(page("HackFlow - команды", content))


def team_detail(request: HttpRequest, team_id: int) -> HttpResponse:
    """Show a single team by id."""
    hackathon, teams_list, submissions = load_project_data()
    team = find_team_by_id(teams_list, team_id)
    if team is None:
        content = """
<h1 class="text-danger">Команда не найдена</h1>
<a href="/teams/" class="btn btn-outline-secondary">К списку команд</a>
"""
        return HttpResponse(page("Команда не найдена", content), status=404)

    submission = None
    for item in submissions:
        if item.team_id == team.id:
            submission = item
            break

    status = "зарегистрирована" if team.is_registered() else "отменена"
    badge = "bg-success" if team.is_registered() else "bg-secondary"
    participants = "".join(
        f'<li class="list-group-item">{participant}</li>'
        for participant in team.participants
    )
    project_html = "<p>Проект еще не сдан.</p>"
    if submission is not None:
        project_html = (
            f'<a href="/submissions/{submission.team_id}/">'
            f"{submission.project_name}</a>"
        )

    content = f"""
<div class="card">
  <div class="card-body">
    <h1 class="card-title h3">{team.name}</h1>
    <p>
      <strong>Статус:</strong>
      <span class="badge {badge}">{status}</span>
    </p>
    <p><strong>Организационный взнос:</strong>
      {team.calculate_participation_fee(hackathon):.0f} руб.
    </p>
    <h2 class="h5">Участники</h2>
    <ul class="list-group mb-3">{participants}</ul>
    <h2 class="h5">Проект</h2>
    {project_html}
    <a href="/teams/" class="btn btn-outline-secondary">К списку команд</a>
  </div>
</div>
"""
    return HttpResponse(page(team.name, content))
