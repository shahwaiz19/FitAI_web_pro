import pandas as pd
import random
import os
import matplotlib.pyplot as plt
import uuid
import joblib
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from ml_models.workout_plan.workout_suggestion_model import WorkoutSuggestionGenerator
from ml_models.diet_plan.diet_plan_model import DietPlanGenerator

# Path to the datasets
DATA_DIR = os.path.join(settings.BASE_DIR, 'data')

def load_and_preprocess_data():
    """
    Load the USDA nutrient dataset and preprocess it.
    Since we have pickle files, we'll create a sample dataset for fallback.
    """
    # Create a sample dataset since we don't have the CSV file
    sample_data = {
        'food_name': [
            'Chicken Breast', 'Brown Rice', 'Broccoli', 'Sweet Potato', 'Greek Yogurt',
            'Salmon', 'Quinoa', 'Spinach', 'Banana', 'Almonds',
            'Eggs', 'Oats', 'Avocado', 'Blueberries', 'Cottage Cheese',
            'Turkey', 'Lentils', 'Kale', 'Apple', 'Walnuts'
        ],
        'category': [
            'Protein', 'Grain', 'Vegetable', 'Vegetable', 'Dairy',
            'Protein', 'Grain', 'Vegetable', 'Fruit', 'Nut',
            'Protein', 'Grain', 'Fruit', 'Fruit', 'Dairy',
            'Protein', 'Legume', 'Vegetable', 'Fruit', 'Nut'
        ],
        'calories': [165, 123, 34, 86, 100, 208, 120, 23, 89, 164, 155, 68, 234, 57, 98, 135, 116, 33, 52, 185],
        'protein_g': [31, 2.6, 2.8, 2, 17, 25, 4.4, 2.9, 1.1, 6, 13, 2.4, 2.9, 0.7, 11, 30, 9, 2.9, 0.3, 4.3],
        'carbs_g': [0, 26, 7, 20, 6, 0, 22, 4, 23, 6, 1, 12, 12, 14, 3, 0, 20, 7, 14, 4],
        'fats_g': [3.6, 1, 0.4, 0.1, 0, 12, 1.9, 0.4, 0.3, 14, 11, 1.4, 21, 0.3, 4, 1, 0.4, 0.5, 0.2, 18],
        'fiber_g': [0, 1.8, 2.6, 3, 0, 0, 3, 2.2, 2.6, 3.5, 0, 1.7, 10, 2.4, 0, 0, 8, 2.6, 2.4, 2],
        'sugar_g': [0, 0.4, 1.7, 4.2, 4, 0, 0, 0.4, 12, 1.2, 1.1, 0.5, 0.3, 10, 3, 0, 2, 0.9, 10, 0.7],
        'sodium_mg': [74, 1, 33, 55, 36, 59, 7, 79, 1, 1, 124, 2, 10, 1, 364, 99, 2, 43, 1, 1],
        'potassium_mg': [256, 43, 316, 337, 141, 490, 172, 558, 358, 208, 126, 61, 485, 77, 104, 239, 369, 447, 107, 125],
        'calcium_mg': [15, 10, 47, 30, 110, 12, 17, 99, 5, 76, 56, 8, 12, 6, 83, 8, 19, 135, 6, 28],
        'iron_mg': [0.9, 0.4, 0.7, 0.6, 0.1, 0.8, 1.5, 2.7, 0.3, 1.0, 1.8, 0.8, 0.6, 0.3, 0.1, 1.4, 3.3, 1.7, 0.1, 0.8],
        'vitamin_c_mg': [0, 0, 89, 2.4, 0, 0, 0, 28, 8.7, 0, 0, 0, 10, 9.7, 0, 0, 4.4, 120, 4.6, 0.4],
        'vitamin_a_iu': [0, 0, 623, 14187, 0, 26, 0, 9377, 64, 0, 540, 0, 146, 54, 37, 0, 68, 10302, 54, 0],
        'cholesterol_mg': [85, 0, 0, 0, 0, 55, 0, 0, 0, 0, 373, 0, 0, 0, 17, 84, 0, 0, 0, 0],
        'saturated_fat_g': [1, 0.2, 0.1, 0, 0, 3, 0.2, 0.1, 0.1, 1.1, 3.3, 0.3, 3, 0, 2.6, 0.2, 0.1, 0.1, 0, 1.7],
        'trans_fat_g': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }

    df = pd.DataFrame(sample_data)
    return df

def select_foods_for_meal(df_filtered, target_calories, meal_name):
    """
    Select foods for a meal to approximate the target calories.
    Uses a simple greedy approach: randomly select foods until close to target.
    """
    selected_foods = []
    total_calories = 0
    total_nutrients = {col: 0 for col in ['protein_g', 'carbs_g', 'fats_g', 'fiber_g', 'sugar_g', 'sodium_mg',
                                         'potassium_mg', 'calcium_mg', 'iron_mg', 'vitamin_c_mg', 'vitamin_a_iu',
                                         'cholesterol_mg', 'saturated_fat_g', 'trans_fat_g']}
    # Sort by calories for greedy selection
    df_sorted = df_filtered.sort_values('calories').reset_index(drop=True)
    # Randomly select up to 5 foods
    num_foods = min(5, len(df_sorted))
    indices = random.sample(range(len(df_sorted)), num_foods)
    for idx in indices:
        food = df_sorted.iloc[idx]
        selected_foods.append({
            'name': food['food_name'],
            'calories': food['calories'],
            'nutrients': {col: food[col] for col in total_nutrients.keys()},
            'category': food['category'],
            'protein_g': food['protein_g'],
            'carbs_g': food['carbs_g'],
            'fats_g': food['fats_g'],
            'fiber_g': food['fiber_g']
        })
        total_calories += food['calories']
        for col in total_nutrients:
            total_nutrients[col] += food[col]
        # If close enough (within 50 calories), stop
        if abs(total_calories - target_calories) <= 50:
            break
    return selected_foods, total_calories, total_nutrients

def generate_diet_plan(required_calories, diet_type='balanced'):
    """
    Generate a 3-meal diet plan based on required daily calories and diet type.

    Args:
        required_calories (int): Total daily calories required.
        diet_type (str): Type of diet ('balanced', 'protein_rich', 'low_carb').

    Returns:
        dict: Structured diet plan with meals, foods, and totals.
    """
    # Set random seed for reproducibility
    random.seed(42)

    df = load_and_preprocess_data()

    # Filter by diet type
    if diet_type == 'protein_rich':
        df_filtered = df[df['protein_g'] > 15]
    elif diet_type == 'low_carb':
        df_filtered = df[df['carbs_g'] < 20]
    else:  # balanced
        df_filtered = df

    if df_filtered.empty:
        return {'error': f'No foods available for the selected diet type: {diet_type}'}

    # Split calories
    breakfast_cal = int(required_calories * 0.3)
    lunch_cal = int(required_calories * 0.4)
    dinner_cal = int(required_calories * 0.3)

    # Generate meals
    breakfast_foods, breakfast_total_cal, breakfast_nutrients = select_foods_for_meal(df_filtered, breakfast_cal, 'Breakfast')
    lunch_foods, lunch_total_cal, lunch_nutrients = select_foods_for_meal(df_filtered, lunch_cal, 'Lunch')
    dinner_foods, dinner_total_cal, dinner_nutrients = select_foods_for_meal(df_filtered, dinner_cal, 'Dinner')

    # Daily totals
    daily_calories = breakfast_total_cal + lunch_total_cal + dinner_total_cal
    daily_nutrients = {k: breakfast_nutrients[k] + lunch_nutrients[k] + dinner_nutrients[k] for k in breakfast_nutrients}

    # Calculate total macros for percentage calculation
    all_foods = breakfast_foods + lunch_foods + dinner_foods
    total_protein = sum(food['protein_g'] for food in all_foods)
    total_carbs = sum(food['carbs_g'] for food in all_foods)
    total_fats = sum(food['fats_g'] for food in all_foods)

    # Generate plots
    plot_id = str(uuid.uuid4())
    static_dir = os.path.join(settings.BASE_DIR, 'static')
    os.makedirs(static_dir, exist_ok=True)

    # Pie chart for calorie distribution
    labels = ['Breakfast', 'Lunch', 'Dinner']
    sizes = [breakfast_total_cal, lunch_total_cal, dinner_total_cal]
    colors = ['#ff9999','#66b3ff','#99ff99']
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Calorie Distribution Among Meals')
    plt.axis('equal')
    pie_chart_path = os.path.join(static_dir, f'calorie_distribution_{plot_id}.png')
    plt.savefig(pie_chart_path)
    plt.close()

    # Bar chart for daily nutrients
    nutrients = ['protein_g', 'carbs_g', 'fats_g', 'fiber_g']
    values = [daily_nutrients[n] for n in nutrients]
    plt.figure(figsize=(8, 6))
    plt.bar(nutrients, values, color='skyblue')
    plt.title('Daily Nutrient Intake')
    plt.xlabel('Nutrients')
    plt.ylabel('Amount (g)')
    bar_chart_path = os.path.join(static_dir, f'nutrient_intake_{plot_id}.png')
    plt.savefig(bar_chart_path)
    plt.close()

    plan = {
        'breakfast': {
            'foods': breakfast_foods,
            'total_calories': breakfast_total_cal,
            'nutrients': breakfast_nutrients
        },
        'lunch': {
            'foods': lunch_foods,
            'total_calories': lunch_total_cal,
            'nutrients': lunch_nutrients
        },
        'dinner': {
            'foods': dinner_foods,
            'total_calories': dinner_total_cal,
            'nutrients': dinner_nutrients
        },
        'daily_totals': {
            'calories': daily_calories,
            'nutrients': daily_nutrients
        },
        'plots': {
            'calorie_distribution': f'calorie_distribution_{plot_id}.png',
            'nutrient_intake': f'nutrient_intake_{plot_id}.png'
        },
        'total_calories': daily_calories,
        'total_protein': total_protein,
        'total_carbs': total_carbs,
        'total_fats': total_fats,
        'protein_percentage': (total_protein * 4 / daily_calories * 100) if daily_calories > 0 else 0,
        'carbs_percentage': (total_carbs * 4 / daily_calories * 100) if daily_calories > 0 else 0,
        'fats_percentage': (total_fats * 9 / daily_calories * 100) if daily_calories > 0 else 0
    }

    return plan

def generate_workout_suggestions(calories_burned, tolerance=50):
    """
    Generate a list of workout suggestions based on calories burned.
    Since we have pickle files, we'll create sample workout data for fallback.
    Args:
        calories_burned (int or float): Target calories burned.
        tolerance (int): Acceptable range around target calories to filter workouts.
    Returns:
        list of dict: Each dict contains activity_type, daily_steps, duration, and calories_burned.
    """
    # Create sample workout data since we don't have the CSV file
    sample_workouts = [
        {'activity_type': 'Running', 'daily_steps': 8000, 'duration_minutes': 45, 'calories_burned': 350, 'intensity': 'High'},
        {'activity_type': 'Cycling', 'daily_steps': 0, 'duration_minutes': 60, 'calories_burned': 280, 'intensity': 'Medium'},
        {'activity_type': 'Swimming', 'daily_steps': 0, 'duration_minutes': 40, 'calories_burned': 320, 'intensity': 'High'},
        {'activity_type': 'Walking', 'daily_steps': 10000, 'duration_minutes': 75, 'calories_burned': 250, 'intensity': 'Low'},
        {'activity_type': 'Weight Training', 'daily_steps': 2000, 'duration_minutes': 50, 'calories_burned': 180, 'intensity': 'Medium'},
        {'activity_type': 'Yoga', 'daily_steps': 1000, 'duration_minutes': 60, 'calories_burned': 120, 'intensity': 'Low'},
        {'activity_type': 'HIIT', 'daily_steps': 3000, 'duration_minutes': 30, 'calories_burned': 300, 'intensity': 'High'},
        {'activity_type': 'Dancing', 'daily_steps': 4000, 'duration_minutes': 45, 'calories_burned': 200, 'intensity': 'Medium'},
        {'activity_type': 'Tennis', 'daily_steps': 5000, 'duration_minutes': 60, 'calories_burned': 400, 'intensity': 'High'},
        {'activity_type': 'Pilates', 'daily_steps': 1500, 'duration_minutes': 50, 'calories_burned': 150, 'intensity': 'Low'}
    ]

    df = pd.DataFrame(sample_workouts)

    # Filter workouts within the tolerance range of calories burned
    filtered_df = df[(df['calories_burned'] >= calories_burned - tolerance) &
                     (df['calories_burned'] <= calories_burned + tolerance)]

    # If no workouts found in range, relax tolerance
    if filtered_df.empty:
        filtered_df = df.copy()

    # Select up to 5 random workouts
    suggestions = filtered_df.sample(n=min(5, len(filtered_df)), random_state=42)

    # Format suggestions as list of dicts
    workout_list = []
    for _, row in suggestions.iterrows():
        workout_list.append({
            'activity_type': row['activity_type'],
            'daily_steps': int(row['daily_steps']),
            'duration': int(row['duration_minutes']),
            'calories_burned': int(row['calories_burned']),
            'intensity': row.get('intensity', 'N/A')
        })

    return workout_list

def calculate_bmr_tdee(age, gender, weight, height, activity_level):
    """
    Calculate BMR using Mifflin-St Jeor Equation and TDEE based on activity level
    """
    # Calculate BMR
    if gender == 'male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # Activity level multipliers
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'extremely_active': 1.9
    }

    tdee = bmr * activity_multipliers.get(activity_level, 1.2)
    return bmr, tdee

def diet_plan_view(request):
    if request.method == 'POST':
        # Get form data
        age = int(request.POST.get('age', 25))
        gender = request.POST.get('gender', 'male')
        weight = float(request.POST.get('weight', 70))
        height = int(request.POST.get('height', 170))
        goal = request.POST.get('goal', 'maintain_weight')
        activity_level = request.POST.get('activity_level', 'moderately_active')
        diet_type = request.POST.get('diet_type', 'balanced')
        allergies = request.POST.get('allergies', '')
        medical_conditions = request.POST.get('medical_conditions', '')

        # Calculate personalized calorie needs
        bmr, tdee = calculate_bmr_tdee(age, gender, weight, height, activity_level)

        # Adjust calories based on goal
        if goal == 'lose_weight':
            required_calories = int(tdee - 500)  # 500 calorie deficit
        elif goal == 'gain_weight':
            required_calories = int(tdee + 500)  # 500 calorie surplus
        elif goal == 'build_muscle':
            required_calories = int(tdee + 300)  # 300 calorie surplus
        else:  # maintain_weight
            required_calories = int(tdee)

        # Ensure minimum calories
        required_calories = max(required_calories, 1200)

        # Try to use ML model first, fallback to rule-based if model not available
        try:
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'diet_plan', 'diet_plan_generator.pkl')
            if os.path.exists(model_path):
                model = DietPlanGenerator.load_model(model_path)
                plan = model.generate_daily_plan(required_calories, diet_type)
            else:
                plan = generate_diet_plan(required_calories, diet_type)
        except Exception as e:
            print(f"Error using ML model: {e}")
            plan = generate_diet_plan(required_calories, diet_type)

        # Add user information to context
        context = {
            'plan': plan,
            'diet_type': diet_type,
            'user_info': {
                'age': age,
                'gender': gender,
                'weight': weight,
                'height': height,
                'goal': goal.replace('_', ' '),
                'activity_level': activity_level.replace('_', ' '),
                'bmr': int(bmr),
                'tdee': int(tdee),
                'target_calories': required_calories,
                'allergies': allergies,
                'medical_conditions': medical_conditions
            }
        }

        return render(request, 'diet_plan_results.html', context)
    else:
        # Show the form
        return render(request, 'diet_plan_form.html')

def workout_plan_view(request):
    if request.method == 'POST':
        calories_burned = int(request.POST.get('calories_burned', 300))

        # Try to use ML model first, fallback to rule-based if model not available
        try:
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'workout_plan', 'workout_suggestion_generator.pkl')
            if os.path.exists(model_path):
                model = WorkoutSuggestionGenerator.load_model(model_path)
                suggestions = model.generate_workout_suggestions(calories_burned)
            else:
                suggestions = generate_workout_suggestions(calories_burned)
        except Exception as e:
            print(f"Error using ML model: {e}")
            suggestions = generate_workout_suggestions(calories_burned)

        return render(request, 'workout_plan.html', {'suggestions': suggestions})
    else:
        # Try to use ML model first, fallback to rule-based if model not available
        try:
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'workout_plan', 'workout_suggestion_generator.pkl')
            if os.path.exists(model_path):
                model = WorkoutSuggestionGenerator.load_model(model_path)
                suggestions = model.generate_workout_suggestions(300)
            else:
                suggestions = generate_workout_suggestions(300)
        except Exception as e:
            print(f"Error using ML model: {e}")
            suggestions = generate_workout_suggestions(300)

        return render(request, 'workout_plan.html', {'suggestions': suggestions})
