import joblib
import os
from django.shortcuts import render

# Correct path for your pickle file - going up two directories from fitness_diet/fitness_diet/
MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "ml_models", "workout_plan", "workout_suggestion_generator.pkl"
)

# Load model with fallback
try:
    workout_model = joblib.load(MODEL_PATH)
    print(f"Successfully loaded ML model from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading ML model: {e}")
    # Create a fallback model
    from ml_models.workout_plan.workout_suggestion_model import WorkoutSuggestionGenerator
    workout_model = WorkoutSuggestionGenerator()
    print("Using fallback model")

def workout_plan_view(request):
    prediction = None
    if request.method == "POST":
        age = int(request.POST.get("age"))
        weight = float(request.POST.get("weight"))
        height = float(request.POST.get("height"))
        fitness_goal = request.POST.get("goal")

        # Example feature vector (change if your model trained differently)
        features = [[age, weight, height]]
        prediction = workout_model.predict(features)[0]

    return render(request, "workout_plan.html", {"prediction": prediction})
