import pytest

from hackflow.teams import (
    Hackathon,
    Team,
    add_team_registration,
    cancel_team_registration,
    calculate_participation_fee,
    count_registered_teams,
    find_teams_by_name,
    is_registration_available,
    sort_teams_by_name,
)


def test_team_object_and_json_conversion():
    team = Team(1, "CodePulse", ["Артем", "Иван"], has_student_discount=True)

    data = team.to_data()
    restored_team = Team.from_data(data)

    assert restored_team.id == 1
    assert restored_team.name == "CodePulse"
    assert restored_team.is_registered() is True
    assert "CodePulse" in str(restored_team)


def test_hackathon_links_team_objects():
    teams = [Team(1, "CodePulse", ["Артем"], has_student_discount=True)]
    hackathon = Hackathon(
        hackathon_id=1,
        name="MIREA Hack 2026",
        max_teams=2,
        registration_is_open=True,
        fee_per_participant=700,
        student_discount_percent=20,
        submission_deadline="2026-09-16 20:00",
        passing_score=22,
        teams=teams,
    )

    new_team = hackathon.create_team("DataStorm", ["Анна", "Кирилл"], True)

    assert hackathon.find_team_by_id(new_team.id) is new_team
    assert hackathon.count_registered_teams() == 2
    assert hackathon.is_registration_available() is False


def test_add_and_cancel_team_registration_for_dicts():
    hackathon = {
        "max_teams": 2,
        "registration_is_open": True,
        "fee_per_participant": 700,
        "student_discount_percent": 20,
    }
    teams = [
        {
            "id": 1,
            "name": "CodePulse",
            "participants": ["Артем", "Иван"],
            "status": "registered",
            "has_student_discount": True,
        }
    ]

    assert is_registration_available(hackathon, teams) is True

    new_team = add_team_registration(
        hackathon,
        teams,
        "DataStorm",
        ["Анна", "Кирилл"],
        True,
    )
    cancelled_team = cancel_team_registration(teams, int(new_team["id"]))

    assert count_registered_teams(teams) == 1
    assert cancelled_team["status"] == "cancelled"


def test_duplicate_team_registration_raises_error():
    hackathon = {"max_teams": 5, "registration_is_open": True}
    teams = [
        {
            "id": 1,
            "name": "CodePulse",
            "participants": ["Артем"],
            "status": "registered",
            "has_student_discount": True,
        }
    ]

    with pytest.raises(ValueError):
        add_team_registration(hackathon, teams, "CodePulse", ["Иван"], False)


def test_search_sort_and_fee_calculation():
    hackathon = {
        "fee_per_participant": 700,
        "student_discount_percent": 20,
    }
    teams = [
        Team(2, "DataStorm", ["Анна", "Кирилл"], has_student_discount=False),
        Team(
            1,
            "CodePulse",
            ["Артем", "Иван", "Мария"],
            has_student_discount=True,
        ),
    ]

    sorted_teams = sort_teams_by_name(teams)
    found_teams = find_teams_by_name(teams, "code")
    fee = calculate_participation_fee(teams[1], hackathon)

    assert sorted_teams[0].name == "CodePulse"
    assert len(found_teams) == 1
    assert fee == 1680
