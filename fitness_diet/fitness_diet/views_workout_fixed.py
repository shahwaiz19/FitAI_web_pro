import os
import joblib
from django.shortcuts import render
from django.conf import settings

# Load the workout suggestion model
model_path = os.path.join(settings.BASE_DIR, "ml_models/workout_plan/workout_suggestion_generator.pkl")
model = joblib.load(model_path)

def workout_view(request):
    suggestions = None
    calories_input = None

    if request.method == "POST":
        try:
            calories_input = int(request.POST.get("calories"))
            suggestions = model.generate_workout_suggestions(calories_input)
        except Exception as e:
            suggestions = [{"error": f"Error: {e}"}]

    return render(request, "workout_plan.html", {
        "suggestions": suggestions,
        "calories_input": calories_input
    })
