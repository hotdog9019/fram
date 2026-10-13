import os

import django
from django.test import Client


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hackflow_site.settings")
django.setup()


def test_homepage_uses_hackflow_data():
    client = Client()

    response = client.get("/")

    assert response.status_code == 200
    assert "HackFlow" in response.content.decode("utf-8")
    assert "Команды" in response.content.decode("utf-8")


def test_team_detail_page():
    client = Client()

    response = client.get("/teams/1/")

    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "CodePulse" in content
    assert "Организационный взнос" in content


def test_submission_detail_page():
    client = Client()

    response = client.get("/submissions/1/")

    assert response.status_code == 200
    content = response.content.decode("utf-8")
    assert "HackFlow Portal" in content
    assert "Решение жюри" in content


def test_missing_team_returns_404():
    client = Client()

    response = client.get("/teams/999/")

    assert response.status_code == 404
    assert "Команда не найдена" in response.content.decode("utf-8")
