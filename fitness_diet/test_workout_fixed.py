#!/usr/bin/env python3
"""
Test script to verify workout model functionality
"""

import os
import sys
import joblib
import numpy as np

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_model_loading():
    """Test if the workout model can be loaded successfully"""
    model_path = 'ml_models/workout_plan/workout_suggestion_generator.pkl'

    print(f"Testing model loading from: {model_path}")
    print(f"Current working directory: {os.getcwd()}")

    if not os.path.exists(model_path):
        print(f"❌ Model file not found at: {model_path}")
        return False

    try:
        # Try to load the model
        model = joblib.load(model_path)
        print("✅ Model loaded successfully")
        print(f"   Model type: {type(model)}")

        # Test prediction
        test_features = [[25, 70, 175]]  # age, weight, height
        prediction = model.predict(test_features)
        print(f"✅ Prediction successful: {prediction[0]}")

        return True

    except Exception as e:
        print(f"❌ Error loading or using model: {e}")
        return False

def test_model_class():
    """Test the WorkoutSuggestionGenerator class directly"""
    try:
        from ml_models.workout_plan.workout_suggestion_model import WorkoutSuggestionGenerator

        model = WorkoutSuggestionGenerator()
        test_features = [[25, 70, 175], [50, 85, 180], [30, 60, 165]]

        predictions = model.predict(test_features)
        print("✅ Direct class test successful:")
        for i, pred in enumerate(predictions):
            print(f"   Test {i+1}: {pred}")

        return True

    except Exception as e:
        print(f"❌ Error testing model class: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing Workout Model Functionality")
    print("=" * 50)

    # Test 1: Load the pickle file
    print("\n1. Testing model file loading:")
    pickle_success = test_model_loading()

    # Test 2: Test the class directly
    print("\n2. Testing model class directly:")
    class_success = test_model_class()

    print("\n" + "=" * 50)
    if pickle_success or class_success:
        print("✅ At least one test passed - model functionality is working")
    else:
        print("❌ All tests failed - there may be an issue with the model")
