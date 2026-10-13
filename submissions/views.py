from django.http import HttpRequest, HttpResponse

from hackflow.submissions import (
    find_submission_by_team_id,
    get_jury_decision,
    get_submission_status,
    sort_projects_by_score,
)
from homepage.views import load_project_data, page


def submissions(request: HttpRequest) -> HttpResponse:
    """Show all project submissions."""
    hackathon, teams, submissions_list = load_project_data()
    items = ""
    for submission in sort_projects_by_score(submissions_list):
        total_score = submission.calculate_total_score()
        finalist = total_score >= hackathon.passing_score
        badge = "bg-success" if finalist else "bg-warning text-dark"
        status = "финал" if finalist else "доработка"
        items += f"""
<li class="list-group-item d-flex justify-content-between align-items-center">
  <a href="/submissions/{submission.team_id}/">
    {submission.project_name}
  </a>
  <span>
    <span class="badge {badge} me-2">{status}</span>
    {total_score:.1f}
  </span>
</li>
"""

    content = f"""
<h1>Сданные проекты</h1>
<p class="text-muted">Всего команд: {len(teams)}.</p>
<ul class="list-group">{items}</ul>
"""
    return HttpResponse(page("HackFlow - проекты", content))


def submission_detail(request: HttpRequest, team_id: int) -> HttpResponse:
    """Show a project submission by team id."""
    hackathon, teams, submissions_list = load_project_data()
    submission = find_submission_by_team_id(submissions_list, team_id)
    if submission is None:
        content = """
<h1 class="text-danger">Проект не найден</h1>
<a href="/submissions/" class="btn btn-outline-secondary">
  К списку проектов
</a>
"""
        return HttpResponse(page("Проект не найден", content), status=404)

    scores = "".join(
        f'<li class="list-group-item">{name}: {score:.1f}</li>'
        for name, score in submission.scores.items()
    )
    status = get_submission_status(submission, hackathon)
    decision = get_jury_decision(
        submission.calculate_total_score(),
        hackathon.passing_score,
    )
    content = f"""
<div class="card">
  <div class="card-body">
    <h1 class="card-title h3">{submission.project_name}</h1>
    <p><strong>Команда:</strong> {submission.team.name}</p>
    <p><strong>Время сдачи:</strong> {submission.submitted_at}</p>
    <p><strong>Статус сдачи:</strong> {status}</p>
    <p><strong>Решение жюри:</strong> {decision}</p>
    <h2 class="h5">Оценки</h2>
    <ul class="list-group mb-3">{scores}</ul>
    <a href="/submissions/" class="btn btn-outline-secondary">
      К списку проектов
    </a>
  </div>
</div>
"""
    return HttpResponse(page(submission.project_name, content))
