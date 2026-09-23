import pytest

from hackflow.teams import (
    add_team_registration,
    cancel_team_registration,
    calculate_participation_fee,
    count_registered_teams,
    find_teams_by_name,
    is_registration_available,
    sort_teams_by_name,
)


def test_add_and_cancel_team_registration():
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
            "participants": ["Артём", "Иван"],
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
            "participants": ["Артём"],
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
        {
            "id": 2,
            "name": "DataStorm",
            "participants": ["Анна", "Кирилл"],
            "status": "registered",
            "has_student_discount": False,
        },
        {
            "id": 1,
            "name": "CodePulse",
            "participants": ["Артём", "Иван", "Мария"],
            "status": "registered",
            "has_student_discount": True,
        },
    ]

    sorted_teams = sort_teams_by_name(teams)
    found_teams = find_teams_by_name(teams, "code")
    fee = calculate_participation_fee(teams[1], hackathon)

    assert sorted_teams[0]["name"] == "CodePulse"
    assert len(found_teams) == 1
    assert fee == 1680
