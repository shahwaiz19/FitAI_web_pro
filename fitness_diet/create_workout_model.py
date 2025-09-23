#!/usr/bin/env python3
"""
Script to create the workout suggestion model pickle file
"""

import os
import sys
import joblib
from ml_models.workout_plan.workout_suggestion_model import WorkoutSuggestionGenerator

def create_model_pickle():
    """Create the workout model pickle file"""
    model_path = 'ml_models/workout_plan/workout_suggestion_generator.pkl'

    print(f"Creating workout model pickle file at: {model_path}")

    try:
        # Create the model instance
        model = WorkoutSuggestionGenerator()

        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)

        # Save the model
        joblib.dump(model, model_path)
        print("✅ Model pickle file created successfully")

        # Test the saved model
        print("\n🔍 Testing the saved model:")
        loaded_model = joblib.load(model_path)
        test_features = [[25, 70, 175], [50, 85, 180], [30, 60, 165]]
        predictions = loaded_model.predict(test_features)

        print("✅ Saved model test successful:")
        for i, pred in enumerate(predictions):
            print(f"   Test {i+1}: {pred}")

        return True

    except Exception as e:
        print(f"❌ Error creating model pickle: {e}")
        return False

if __name__ == "__main__":
    print("🏋️ Creating Workout Suggestion Model")
    print("=" * 50)

    success = create_model_pickle()

    print("\n" + "=" * 50)
    if success:
        print("✅ Model creation completed successfully!")
        print("The workout generator should now work on the landing page.")
    else:
        print("❌ Model creation failed.")
