from django.urls import path

from . import views


app_name = "teams"

urlpatterns = [
    path("", views.teams, name="teams"),
    path("<int:team_id>/", views.team_detail, name="team_detail"),
]
