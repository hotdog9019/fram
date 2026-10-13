from django.urls import path

from . import views


urlpatterns = [
    path("", views.submissions, name="submissions"),
    path("<int:team_id>/", views.submission_detail, name="submission_detail"),
]
