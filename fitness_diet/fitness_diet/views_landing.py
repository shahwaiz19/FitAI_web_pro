from django.shortcuts import render

def landing_with_workout_view(request):
    return render(request, 'landing_with_workout.html')
