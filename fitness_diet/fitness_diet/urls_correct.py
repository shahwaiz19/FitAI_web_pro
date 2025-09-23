from django.urls import path
from . import views_correct

urlpatterns = [
    path("workout/", views_correct.workout_plan_view, name="workout_plan"),
]
