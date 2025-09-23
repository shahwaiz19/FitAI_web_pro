from django.urls import path
from .views_rule_based_fixed import diet_plan_view, workout_plan_view

urlpatterns = [
    path('diet_plan/', diet_plan_view, name='diet_plan'),
    path('workout_plan/', workout_plan_view, name='workout_plan'),
]
