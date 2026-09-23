from hackflow.statistics import build_hackathon_statistics
from hackflow.submissions import (
    calculate_average_score,
    calculate_total_score,
    get_finalist_submissions,
    get_jury_decision,
    get_submission_status,
    sort_projects_by_score,
)


def test_submission_scoring_and_decision():
    scores = {"idea": 8.5, "prototype": 9.0, "presentation": 7.5}

    total_score = calculate_total_score(scores)
    average_score = calculate_average_score(scores)
    decision = get_jury_decision(total_score, 22)

    assert total_score == 25.0
    assert round(average_score, 2) == 8.33
    assert "проходит в финал" in decision


def test_submission_status_and_sorting():
    hackathon = {"submission_deadline": "2026-09-16 20:00", "passing_score": 22}
    submissions = [
        {
            "team_id": 1,
            "project_name": "HackFlow Portal",
            "submitted_at": "2026-09-16 18:20",
            "scores": {"idea": 8.5, "prototype": 9.0, "presentation": 7.5},
        },
        {
            "team_id": 2,
            "project_name": "Mentor Match",
            "submitted_at": "2026-09-16 20:15",
            "scores": {"idea": 8.0, "prototype": 6.5, "presentation": 7.0},
        },
    ]

    sorted_projects = sort_projects_by_score(submissions)
    finalists = get_finalist_submissions(submissions, hackathon)

    assert get_submission_status(submissions[0], hackathon) == "Проект сдан вовремя"
    assert (
        get_submission_status(submissions[1], hackathon)
        == "Проект сдан после дедлайна"
    )
    assert sorted_projects[0]["project_name"] == "HackFlow Portal"
    assert len(finalists) == 1


def test_hackathon_statistics():
    hackathon = {"passing_score": 22}
    teams = [
        {
            "id": 1,
            "name": "CodePulse",
            "participants": ["Артём", "Иван"],
            "status": "registered",
        },
        {
            "id": 2,
            "name": "Backend Crew",
            "participants": ["Анна"],
            "status": "cancelled",
        },
    ]
    submissions = [
        {
            "team_id": 1,
            "scores": {"idea": 8.5, "prototype": 9.0, "presentation": 7.5},
        }
    ]

    statistics = build_hackathon_statistics(hackathon, teams, submissions)

    assert statistics["registered_teams"] == 1
    assert statistics["cancelled_teams"] == 1
    assert statistics["participants"] == 2
    assert statistics["finalists"] == 1
