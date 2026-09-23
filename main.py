import sys
from copy import deepcopy
from pathlib import Path

from hackflow.statistics import build_hackathon_statistics
from hackflow.storage import load_json
from hackflow.submissions import (
    calculate_average_score,
    calculate_total_score,
    find_submission_by_team_id,
    get_jury_decision,
    get_submission_status,
    sort_projects_by_score,
)
from hackflow.teams import (
    add_team_registration,
    calculate_participation_fee,
    cancel_team_registration,
    find_teams_by_name,
    is_registration_available,
    sort_teams_by_name,
)
from hackflow.utils import format_datetime, parse_datetime


DATA_DIR = Path("data")


def main():
    sys.stdout.reconfigure(encoding="utf-8")

    try:
        hackathon = load_json(DATA_DIR / "hackathon.json")
        teams = load_json(DATA_DIR / "teams.json")
        submissions = load_json(DATA_DIR / "submissions.json")
    except (FileNotFoundError, ValueError) as error:
        print(error)
        return

    team = teams[0]
    submission = find_submission_by_team_id(submissions, int(team["id"]))
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
    cancelled_team = cancel_team_registration(demo_teams, int(new_team["id"]))

    scores = submission["scores"]
    total_score = calculate_total_score(scores)
    average_score = calculate_average_score(scores)
    participation_fee = calculate_participation_fee(team, hackathon)
    submitted_at = parse_datetime(str(submission["submitted_at"]))
    deadline = parse_datetime(str(hackathon["submission_deadline"]))
    registration_status = "Регистрация доступна"
    if not is_registration_available(hackathon, teams):
        registration_status = "Регистрация недоступна"

    statistics = build_hackathon_statistics(hackathon, teams, submissions)
    sorted_teams = sort_teams_by_name(teams)
    search_results = find_teams_by_name(teams, "code")
    sorted_projects = sort_projects_by_score(submissions)
    jury_decision = get_jury_decision(
        total_score,
        float(hackathon["passing_score"]),
    )

    print(f"Хакатон: {hackathon['name']}")
    print(f"Команда: {team['name']}")
    print(f"Участников в команде: {len(team['participants'])}")
    print(f"Статус регистрации: {registration_status}")
    print(f"Организационный взнос: {participation_fee:.0f} руб.")
    print(f"Срок сдачи проекта: {format_datetime(deadline)}")
    print(f"Фактическая сдача: {format_datetime(submitted_at)}")
    print(f"Статус сдачи: {get_submission_status(submission, hackathon)}")
    print(f"Средний балл жюри: {average_score:.2f}")
    print(jury_decision)
    print(f"Новая заявка: {new_team['name']}")
    print(f"Отмена заявки: {cancelled_team['status']}")
    print(f"Команды по алфавиту: {', '.join(team['name'] for team in sorted_teams)}")
    print(f"Поиск по 'code': {len(search_results)} команда")
    print(f"Лучший проект: {sorted_projects[0]['project_name']}")
    print(f"Финалистов: {statistics['finalists']}")


if __name__ == "__main__":
    main()
