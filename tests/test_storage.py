import pytest

from hackflow.storage import (
    load_json,
    load_submissions,
    load_teams,
    save_json,
    save_submissions,
    save_teams,
)
from hackflow.submissions import Submission
from hackflow.teams import Team


def test_save_and_load_json(tmp_path):
    data_path = tmp_path / "teams.json"
    data = [{"id": 1, "name": "CodePulse"}]

    save_json(data_path, data)
    loaded_data = load_json(data_path)

    assert loaded_data == data


def test_invalid_json_raises_error(tmp_path):
    data_path = tmp_path / "broken.json"
    data_path.write_text("{invalid", encoding="utf-8")

    with pytest.raises(ValueError):
        load_json(data_path)


def test_save_and_load_team_objects(tmp_path):
    data_path = tmp_path / "teams.json"
    teams = [Team(1, "CodePulse", ["Артем", "Иван"], has_student_discount=True)]

    save_teams(data_path, teams)
    loaded_teams = load_teams(data_path)

    assert loaded_teams[0].name == "CodePulse"
    assert loaded_teams[0].participants == ["Артем", "Иван"]


def test_save_and_load_submission_objects(tmp_path):
    data_path = tmp_path / "submissions.json"
    teams = [Team(1, "CodePulse", ["Артем"])]
    submissions = [
        Submission(
            teams[0],
            "HackFlow Portal",
            "2026-09-16 18:20",
            {"idea": 8.5},
        )
    ]

    save_submissions(data_path, submissions)
    loaded_submissions = load_submissions(data_path, teams)

    assert loaded_submissions[0].team is teams[0]
    assert loaded_submissions[0].project_name == "HackFlow Portal"
