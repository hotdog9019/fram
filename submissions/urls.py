from django.urls import path

from . import views


app_name = "submissions"

urlpatterns = [
    path("", views.submissions, name="submissions"),
    path("<int:team_id>/", views.submission_detail, name="submission_detail"),
]
