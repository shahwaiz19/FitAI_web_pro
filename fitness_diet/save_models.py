#!/usr/bin/env python3
"""
Script to save the ML models to pickle files for the Django application.
This script creates and saves both diet plan and workout suggestion models.
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

def save_diet_model():
    """Save the advanced diet plan model to a pickle file"""
    print("=== SAVING ADVANCED DIET PLAN MODEL ===\n")

    try:
        # Create the model
        print("Creating advanced diet plan model with K-Means clustering...")
        model = DietPlanGenerator()
        print("✓ Advanced diet plan model created successfully\n")

        # Display model information
        print("--- Model Information ---")
        info = model.get_model_info()
        if "error" not in info:
            print(f"Dataset loaded: {info['dataset_shape']}")
            print(f"Total foods available: {info['total_foods']}")
            print(f"Categories: {len(info['categories'])} different categories")
            print(f"Model type: {info['model_type']}")
            print(f"Features used: {', '.join(info['features_used'])}")
            print(f"Calorie range: {info['calorie_range']['min']:.0f} - {info['calorie_range']['max']:.0f} calories")
        else:
            print(f"Error: {info['error']}")
            return False
        print()

        # Save the model
        model_path = 'ml_models/diet_plan/diet_plan_generator.pkl'
        print(f"Saving model to: {model_path}")

        success = model.save_model(model_path)
        if success:
            print("✓ Advanced diet plan model saved successfully!")
            print(f"Model file location: {os.path.abspath(model_path)}")
        else:
            print("✗ Failed to save diet plan model")
            return False

    except Exception as e:
        print(f"✗ Error creating/saving diet plan model: {e}")
        return False

    return True

def save_workout_model():
    """Save the workout suggestion model to a pickle file"""
    print("\n=== SAVING WORKOUT SUGGESTION MODEL ===\n")

    try:
        # Create the model
        print("Creating workout suggestion model...")
        model = WorkoutSuggestionGenerator()
        print("✓ Workout suggestion model created successfully\n")

        # Display model information
        print("--- Model Information ---")
        info = model.get_model_info()
        if "error" not in info:
            print(f"Dataset loaded: {info['dataset_shape']}")
            print(f"Total workouts available: {info['total_workouts']}")
            print(f"Calorie range: {info['calorie_range']['min']} - {info['calorie_range']['max']} calories")
            print(f"Activity types: {len(info['activity_types'])} different types")
            print(f"Sample activities: {', '.join(info['activity_types'][:5])}...")
        else:
            print(f"Error: {info['error']}")
            return False
        print()

        # Save the model
        model_path = 'ml_models/workout_plan/workout_suggestion_generator.pkl'
        print(f"Saving model to: {model_path}")

        success = model.save_model(model_path)
        if success:
            print("✓ Workout suggestion model saved successfully!")
            print(f"Model file location: {os.path.abspath(model_path)}")
        else:
            print("✗ Failed to save workout suggestion model")
            return False

    except Exception as e:
        print(f"✗ Error creating/saving workout suggestion model: {e}")
        return False

    return True

def test_saved_models():
    """Test loading the saved models"""
    print("\n=== TESTING SAVED MODELS ===\n")

    # Test diet plan model
    print("--- Testing Advanced Diet Plan Model ---")
    try:
        model_path = 'ml_models/diet_plan/diet_plan_generator.pkl'
        if os.path.exists(model_path):
            loaded_model = DietPlanGenerator.load_model(model_path)
            if loaded_model:
                print("✓ Advanced diet plan model loaded successfully!")

                # Quick test with the loaded model
                test_plan = loaded_model.generate_daily_plan(2000, 'balanced')
                if test_plan and 'error' not in test_plan:
                    print("✓ Generated sample diet plan successfully")
                    print(f"  - Total calories: {test_plan['total_calories']:.0f}")
                    print(f"  - Breakfast items: {len(test_plan['breakfast'])}")
                    print(f"  - Lunch items: {len(test_plan['lunch'])}")
                    print(f"  - Dinner items: {len(test_plan['dinner'])}")
                else:
                    print("✗ Failed to generate diet plan")
            else:
                print("✗ Failed to load diet plan model")
        else:
            print("✗ Diet plan model file not found")
    except Exception as e:
        print(f"✗ Error testing diet plan model: {e}")

    # Test workout suggestion model
    print("\n--- Testing Workout Suggestion Model ---")
    try:
        model_path = 'ml_models/workout_plan/workout_suggestion_generator.pkl'
        if os.path.exists(model_path):
            loaded_model = WorkoutSuggestionGenerator.load_model(model_path)
            if loaded_model:
                print("✓ Workout suggestion model loaded successfully!")

                # Quick test with the loaded model
                test_suggestions = loaded_model.generate_workout_suggestions(300)
                if test_suggestions:
                    print("✓ Generated sample workout suggestions successfully")
                    print(f"  - Number of suggestions: {len(test_suggestions)}")
                    print(f"  - Sample activity: {test_suggestions[0]['activity_type']}")
                else:
                    print("✗ Failed to generate workout suggestions")
            else:
                print("✗ Failed to load workout suggestion model")
        else:
            print("✗ Workout suggestion model file not found")
    except Exception as e:
        print(f"✗ Error testing workout suggestion model: {e}")

def main():
    """Main function to save all models"""
    print("=== ADVANCED ML MODEL SAVER FOR FITAI ===\n")
    print("This script will save your advanced ML models:")
    print("- Diet Plan Generator (K-Means clustering)")
    print("- Workout Suggestion Generator")
    print()

    # Save both models
    diet_success = save_diet_model()
    workout_success = save_workout_model()

    if diet_success and workout_success:
        print("\n=== ALL MODELS SAVED SUCCESSFULLY ===")
        print("You can now use the saved models in your Django application!")

        # Test the saved models
        test_saved_models()

        print("\n=== SETUP COMPLETED ===")
        print("Your advanced ML models are ready to use with the Django application.")
        print("The views will automatically use these models when available.")

        return True
    else:
        print("\n=== SOME MODELS FAILED TO SAVE ===")
        print("Please check the errors above and try again.")
        return False

if __name__ == "__main__":
    main()
