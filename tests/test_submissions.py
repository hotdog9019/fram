import pytest

from hackflow.statistics import build_hackathon_statistics
from hackflow.submissions import (
    Submission,
    calculate_average_score,
    calculate_total_score,
    create_submission,
    get_finalist_submissions,
    get_jury_decision,
    get_submission_status,
    sort_projects_by_score,
)
from hackflow.teams import Hackathon, Team


def make_hackathon() -> Hackathon:
    teams = [
        Team(1, "CodePulse", ["Артем", "Иван"]),
        Team(2, "Backend Crew", ["Анна"], status="cancelled"),
    ]
    return Hackathon(
        hackathon_id=1,
        name="MIREA Hack 2026",
        max_teams=5,
        registration_is_open=True,
        fee_per_participant=700,
        student_discount_percent=20,
        submission_deadline="2026-09-16 20:00",
        passing_score=22,
        teams=teams,
    )


def test_submission_object_links_team_and_converts_to_json():
    hackathon = make_hackathon()
    submission = create_submission(
        hackathon,
        hackathon.teams[0],
        "HackFlow Portal",
        "2026-09-16 18:20",
        {"idea": 8.5, "prototype": 9.0, "presentation": 7.5},
    )

    data = submission.to_data()
    restored_submission = Submission.from_data(data, hackathon.teams)

    assert restored_submission.team is hackathon.teams[0]
    assert restored_submission.team_id == 1
    assert restored_submission.calculate_total_score() == 25.0
    assert "HackFlow Portal" in str(restored_submission)


def test_submission_for_cancelled_team_raises_error():
    hackathon = make_hackathon()

    with pytest.raises(ValueError):
        create_submission(
            hackathon,
            hackathon.teams[1],
            "Cancelled Project",
            "2026-09-16 18:20",
            {"idea": 8.0},
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
    hackathon = make_hackathon()
    submissions = [
        Submission(
            hackathon.teams[0],
            "HackFlow Portal",
            "2026-09-16 18:20",
            {"idea": 8.5, "prototype": 9.0, "presentation": 7.5},
        ),
        Submission(
            Team(3, "Mentor Match Team", ["Кирилл"]),
            "Mentor Match",
            "2026-09-16 20:15",
            {"idea": 8.0, "prototype": 6.5, "presentation": 7.0},
        ),
    ]

    sorted_projects = sort_projects_by_score(submissions)
    finalists = get_finalist_submissions(submissions, hackathon)

    assert get_submission_status(submissions[0], hackathon) == "Проект сдан вовремя"
    assert get_submission_status(submissions[1], hackathon) == (
        "Проект сдан после дедлайна"
    )
    assert sorted_projects[0].project_name == "HackFlow Portal"
    assert len(finalists) == 1


def test_hackathon_statistics():
    hackathon = make_hackathon()
    submissions = [
        Submission(
            hackathon.teams[0],
            "HackFlow Portal",
            "2026-09-16 18:20",
            {"idea": 8.5, "prototype": 9.0, "presentation": 7.5},
        )
    ]

    statistics = build_hackathon_statistics(
        hackathon,
        hackathon.teams,
        submissions,
    )

    assert statistics["registered_teams"] == 1
    assert statistics["cancelled_teams"] == 1
    assert statistics["participants"] == 2
    assert statistics["finalists"] == 1
