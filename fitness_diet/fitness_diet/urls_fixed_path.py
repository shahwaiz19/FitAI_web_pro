from django.urls import path
from . import views_fixed_path

urlpatterns = [
    path("workout/", views_fixed_path.workout_plan_view, name="workout_plan"),
]
