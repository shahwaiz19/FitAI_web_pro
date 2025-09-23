"""
URL configuration for fitness_diet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views_updated_final as views
from .views_food_calorie import food_calorie_predictor
from .views_health_prediction import heart_disease_prediction, lung_disease_prediction, heart_disease_page, lung_disease_page
from .views_calories_burnt import calories_burnt_predictor
from .views_meal_customization import customize_meals, swap_meal
from django.views.generic import RedirectView
from . import views_rule_based_fixed

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing'),
    path('landing/', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('onboarding/welcome/', views.onboarding_welcome, name='onboarding_welcome'),
    path('onboarding/goal/', views.onboarding_goal, name='onboarding_goal'),
    path('onboarding/info/', views.onboarding_info, name='onboarding_info'),
    path('onboarding/account/', views.onboarding_account, name='onboarding_account'),
    path('gain-weight-plan/', views.gain_weight_plan, name='gain_weight_plan'),
    path('lose-weight-plan/', views.lose_weight_plan, name='lose_weight_plan'),
    path('food-recognition/', views.food_recognition_page, name='food_recognition'),
    path('food-calorie-predictor/', food_calorie_predictor, name='food_calorie_predictor'),
    path('calories-burnt-predictor/', calories_burnt_predictor, name='calories_burnt_predictor'),
    path('customize-meals/', customize_meals, name='customize_meals'),
    path('swap-meal/', swap_meal, name='swap_meal'),
    # Health Prediction URLs
    path('heart-disease-prediction/', heart_disease_prediction, name='heart_disease_prediction'),
    path('lung-disease-prediction/', lung_disease_prediction, name='lung_disease_prediction'),
    path('heart-disease/', heart_disease_page, name='heart_disease_page'),
    path('lung-disease/', lung_disease_page, name='lung_disease_page'),
    path('accounts/', include('allauth.urls')),
    path('accounts/profile/', views.landing_page, name='account_profile'),

    # Rule-based system URLs (FIXED)
    path('diet_plan/', views_rule_based_fixed.diet_plan_view, name='diet_plan'),
    path('workout_plan/', views_rule_based_fixed.workout_plan_view, name='workout_plan'),

    path('', RedirectView.as_view(url='/landing/', permanent=False)),
]
