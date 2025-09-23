"""
URL configuration for fitness_diet project.
"""
from django.contrib import admin
from django.urls import path, include
from . import views_fixed_workout as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('onboarding/welcome/', views.onboarding_welcome, name='onboarding_welcome'),
    path('onboarding/goal/', views.onboarding_goal, name='onboarding_goal'),
    path('onboarding/info/', views.onboarding_info, name='onboarding_info'),
    path('onboarding/account/', views.onboarding_account, name='onboarding_account'),
    path('gain-weight-plan/', views.gain_weight_plan, name='gain_weight_plan'),
    path('lose-weight-plan/', views.lose_weight_plan, name='lose_weight_plan'),
    path('food-recognition/', views.food_recognition_page, name='food_recognition'),
    path('accounts/', include('allauth.urls')),
]
