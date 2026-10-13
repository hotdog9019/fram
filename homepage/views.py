from django.http import HttpRequest, HttpResponse

from hackflow.statistics import build_hackathon_statistics
from hackflow.storage import load_hackathon, load_submissions, load_teams


def load_project_data():
    """Load HackFlow objects from JSON files."""
    teams = load_teams("data/teams.json")
    hackathon = load_hackathon("data/hackathon.json", teams)
    submissions = load_submissions("data/submissions.json", teams)
    return hackathon, teams, submissions


def page(title: str, content: str) -> str:
    """Build a simple Bootstrap HTML page."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
  <nav class="navbar navbar-expand-lg bg-body-tertiary mb-4">
    <div class="container">
      <a class="navbar-brand" href="/">HackFlow</a>
      <div class="navbar-nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/teams/">Команды</a>
        <a class="nav-link" href="/submissions/">Проекты</a>
      </div>
    </div>
  </nav>
  <main class="container pb-5">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Show project homepage with summary statistics."""
    hackathon, teams, submissions = load_project_data()
    statistics = build_hackathon_statistics(hackathon, teams, submissions)
    content = f"""
<section class="mb-4">
  <h1 class="display-4">HackFlow</h1>
  <p class="lead">
    Веб-интерфейс для организации хакатона {hackathon.name}.
  </p>
  <a href="/teams/" class="btn btn-primary me-2">Команды</a>
  <a href="/submissions/" class="btn btn-secondary">Проекты</a>
</section>
<section class="row g-3">
  <div class="col-md-4">
    <div class="border rounded p-3">
      <h2 class="h5">Команды</h2>
      <p class="fs-3 mb-0">{statistics["registered_teams"]}</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="border rounded p-3">
      <h2 class="h5">Участники</h2>
      <p class="fs-3 mb-0">{statistics["participants"]}</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="border rounded p-3">
      <h2 class="h5">Финалисты</h2>
      <p class="fs-3 mb-0">{statistics["finalists"]}</p>
    </div>
  </div>
</section>
"""
    return HttpResponse(page("HackFlow", content))


def page_not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Return a custom 404 page."""
    content = """
<h1 class="text-danger">404 - страница не найдена</h1>
<p>Проверьте адрес или вернитесь на главную страницу.</p>
<a href="/" class="btn btn-primary">На главную</a>
"""
    return HttpResponse(page("404 - страница не найдена", content), status=404)
