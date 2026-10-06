import sys
from copy import deepcopy
from pathlib import Path

from hackflow.statistics import build_hackathon_statistics
from hackflow.storage import load_hackathon, load_submissions, load_teams
from hackflow.submissions import (
    find_submission_by_team_id,
    get_jury_decision,
    get_submission_status,
    sort_projects_by_score,
)
from hackflow.teams import (
    add_team_registration,
    cancel_team_registration,
    find_teams_by_name,
    is_registration_available,
    sort_teams_by_name,
)
from hackflow.utils import format_datetime, parse_datetime


DATA_DIR = Path("data")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")

    try:
        teams = load_teams(DATA_DIR / "teams.json")
        hackathon = load_hackathon(DATA_DIR / "hackathon.json", teams)
        submissions = load_submissions(DATA_DIR / "submissions.json", teams)
    except (FileNotFoundError, ValueError) as error:
        print(error)
        return

    team = teams[0]
    submission = find_submission_by_team_id(submissions, team.id)
    if submission is None:
        print("Для выбранной команды нет сданного проекта")
        return

    demo_teams = deepcopy(teams)
    new_team = add_team_registration(
        hackathon,
        demo_teams,
        "Frontend Force",
        ["Елена Козлова", "Павел Захаров"],
        True,
    )
    cancelled_team = cancel_team_registration(demo_teams, new_team.id)

    total_score = submission.calculate_total_score()
    average_score = submission.calculate_average_score()
    participation_fee = team.calculate_participation_fee(hackathon)
    submitted_at = parse_datetime(submission.submitted_at)
    deadline = parse_datetime(hackathon.submission_deadline)
    registration_status = "Регистрация доступна"
    if not is_registration_available(hackathon, teams):
        registration_status = "Регистрация недоступна"

    statistics = build_hackathon_statistics(hackathon, teams, submissions)
    sorted_teams = sort_teams_by_name(teams)
    search_results = find_teams_by_name(teams, "code")
    sorted_projects = sort_projects_by_score(submissions)
    jury_decision = get_jury_decision(total_score, hackathon.passing_score)

    print(f"Хакатон: {hackathon.name}")
    print(f"Команда: {team.name}")
    print(f"Участников в команде: {len(team.participants)}")
    print(f"Статус регистрации: {registration_status}")
    print(f"Организационный взнос: {participation_fee:.0f} руб.")
    print(f"Срок сдачи проекта: {format_datetime(deadline)}")
    print(f"Фактическая сдача: {format_datetime(submitted_at)}")
    print(f"Статус сдачи: {get_submission_status(submission, hackathon)}")
    print(f"Средний балл жюри: {average_score:.2f}")
    print(jury_decision)
    print(f"Новая заявка: {new_team.name}")
    print(f"Отмена заявки: {cancelled_team.status}")
    print(f"Команды по алфавиту: {', '.join(team.name for team in sorted_teams)}")
    print(f"Поиск по 'code': {len(search_results)} команда")
    print(f"Лучший проект: {sorted_projects[0].project_name}")
    print(f"Финалистов: {statistics['finalists']}")


if __name__ == "__main__":
    main()
