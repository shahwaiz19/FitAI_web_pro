import pickle
import numpy as np
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
from .models import CalorieCalculation

# Load the calories burnt model
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ml_models', 'calories_burnt', 'calorie_burn_model.pkl')
with open(MODEL_PATH, 'rb') as f:
    calorie_burn_model = pickle.load(f)

@csrf_exempt
def calories_burnt_predictor(request):
    calories_burnt = None
    if request.method == 'POST':
        try:
            data = request.POST
            # Extract input features from POST data
            gender = 1 if data.get('gender', '').lower() == 'male' else 0
            age = float(data.get('age', 25))
            height = float(data.get('height', 170))
            weight = float(data.get('weight', 65))
            duration = float(data.get('duration', 30))
            heart_rate = float(data.get('heart_rate', 120))
            body_temp = float(data.get('body_temp', 37.0))

            # Prepare input array for model
            input_features = np.array([[gender, age, height, weight, duration, heart_rate, body_temp]])

            # Predict calories burnt
            prediction = calorie_burn_model.predict(input_features)
            calories_burnt = round(float(prediction[0]), 1)

            # Save the calorie calculation to database
            try:
                CalorieCalculation.objects.create(
                    age=int(age),
                    height=height,
                    actual_weight=weight,
                    calories_burned=calories_burnt
                )
            except Exception as e:
                print(f"Error saving calorie calculation: {e}")

            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'calories_burnt': calories_burnt})

        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': str(e)}, status=400)
            pass  # Handle error gracefully by showing no result

    return render(request, 'calories_burnt.html', {'calories_burnt': calories_burnt})
