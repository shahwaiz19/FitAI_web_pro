from django.urls import path
from .views_landing import landing_with_workout_view

urlpatterns = [
    path('landing-with-workout/', landing_with_workout_view, name='landing_with_workout'),
]
