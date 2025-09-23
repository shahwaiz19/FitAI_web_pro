#!/usr/bin/env python3
"""
Test script to verify your ML models are working correctly.
Run this script to test both diet plan and workout plan generators.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from ml_models.diet_plan.diet_plan_model import DietPlanGenerator
from ml_models.workout_plan.workout_suggestion_model import WorkoutSuggestionGenerator

def test_diet_plan_model():
    """Test the advanced diet plan generator"""
    print("=== TESTING ADVANCED DIET PLAN GENERATOR ===\n")

    try:
        # Load the model
        model_path = 'ml_models/diet_plan/diet_plan_generator.pkl'
        if os.path.exists(model_path):
            print(f"✓ Found diet plan model at: {model_path}")
            model = DietPlanGenerator.load_model(model_path)
            print("✓ Diet plan model loaded successfully!\n")
        else:
            print(f"✗ Diet plan model not found at: {model_path}")
            return False

        # Display model information
        print("--- Model Information ---")
        info = model.get_model_info()
        if "error" not in info:
            print(f"Dataset shape: {info['dataset_shape']}")
            print(f"Total foods: {info['total_foods']}")
            print(f"Categories: {len(info['categories'])}")
            print(f"Model type: {info['model_type']}")
            print(f"Calorie range: {info['calorie_range']['min']:.0f} - {info['calorie_range']['max']:.0f}")
        else:
            print(f"Error: {info['error']}")
            return False
        print()

        # Test different diet types
        diet_types = ['balanced', 'protein_rich', 'low_carb']
        calorie_levels = [1500, 2000, 2500]

        for diet_type in diet_types:
            for calories in calorie_levels:
                print(f"--- Testing {diet_type.upper()} Diet - {calories} Calories ---")
                try:
                    plan = model.generate_daily_plan(calories, diet_type)
                    if plan and 'error' not in plan:
                        print(f"✓ Generated plan successfully")
                        print(f"  Total calories: {plan['total_calories']:.0f}")
                        print(f"  Breakfast items: {len(plan['breakfast'])}")
                        print(f"  Lunch items: {len(plan['lunch'])}")
                        print(f"  Dinner items: {len(plan['dinner'])}")
                    else:
                        print("✗ Failed to generate plan")
                        return False
                except Exception as e:
                    print(f"✗ Error generating {diet_type} plan: {e}")
                    return False
                print()

        print("✅ All diet plan tests passed!")
        return True

    except Exception as e:
        print(f"✗ Error testing diet plan model: {e}")
        return False

def test_workout_plan_model():
    """Test the workout suggestion generator"""
    print("\n=== TESTING WORKOUT SUGGESTION GENERATOR ===\n")

    try:
        # Load the model
        model_path = 'ml_models/workout_plan/workout_suggestion_generator.pkl'
        if os.path.exists(model_path):
            print(f"✓ Found workout model at: {model_path}")
            model = WorkoutSuggestionGenerator.load_model(model_path)
            print("✓ Workout suggestion model loaded successfully!\n")
        else:
            print(f"✗ Workout model not found at: {model_path}")
            return False

        # Display model information
        print("--- Model Information ---")
        info = model.get_model_info()
        if "error" not in info:
            print(f"Dataset shape: {info['dataset_shape']}")
            print(f"Total workouts: {info['total_workouts']}")
            print(f"Activity types: {len(info['activity_types'])}")
            print(f"Calorie range: {info['calorie_range']['min']} - {info['calorie_range']['max']}")
        else:
            print(f"Error: {info['error']}")
            return False
        print()

        # Test different calorie levels
        calorie_levels = [200, 300, 500, 800]

        for calories in calorie_levels:
            print(f"--- Testing {calories} Calories Burn Target ---")
            try:
                suggestions = model.generate_workout_suggestions(calories)
                if suggestions:
                    print(f"✓ Generated {len(suggestions)} workout suggestions")
                    for i, workout in enumerate(suggestions[:3], 1):  # Show first 3
                        print(f"  {i}. {workout['activity_type']} - {workout['calories_burned']} cal, {workout['duration']} min")
                    if len(suggestions) > 3:
                        print(f"  ... and {len(suggestions) - 3} more suggestions")
                else:
                    print("✗ No workout suggestions generated")
                    return False
            except Exception as e:
                print(f"✗ Error generating workout suggestions: {e}")
                return False
            print()

        print("✅ All workout plan tests passed!")
        return True

    except Exception as e:
        print(f"✗ Error testing workout model: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 TESTING YOUR ML MODELS FOR FITAI\n")
    print("=" * 50)

    # Test both models
    diet_success = test_diet_plan_model()
    workout_success = test_workout_plan_model()

    print("\n" + "=" * 50)
    if diet_success and workout_success:
        print("🎉 ALL TESTS PASSED!")
        print("\nYour ML models are working perfectly!")
        print("\nNext steps:")
        print("1. Start Django server: python manage.py runserver")
        print("2. Visit the landing page to see your features")
        print("3. Test the diet and workout plan generators")
        print("\nYour FitAI application is ready to use!")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    main()
