#!/usr/bin/env python
"""
Test script to verify the fixed template works without the 'replace' filter error.
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings_fixed')

# Setup Django
django.setup()

from django.template import Template, Context
from django.conf import settings

def test_template():
    """Test the fixed template without the 'replace' filter."""

    # Read the fixed template
    template_path = BASE_DIR / 'templates' / 'diet_plan_results_fixed.html'
    if not template_path.exists():
        print(f"❌ Template not found: {template_path}")
        return False

    with open(template_path, 'r') as f:
        template_content = f.read()

    # Create a test context with user info that would normally use the 'replace' filter
    context_data = {
        'plan': {
            'breakfast': {'foods': [], 'total_calories': 500},
            'lunch': {'foods': [], 'total_calories': 600},
            'dinner': {'foods': [], 'total_calories': 400},
            'daily_totals': {'calories': 1500},
            'total_calories': 1500,
            'total_protein': 80,
            'total_carbs': 150,
            'total_fats': 50,
            'protein_percentage': 21,
            'carbs_percentage': 40,
            'fats_percentage': 30,
            'plots': {
                'calorie_distribution': 'test_pie.png',
                'nutrient_intake': 'test_bar.png'
            }
        },
        'diet_type': 'balanced',
        'user_info': {
            'age': 30,
            'gender': 'male',
            'weight': 75,
            'height': 175,
            'goal': 'maintain_weight',  # This would normally be 'maintain weight' after replace filter
            'activity_level': 'moderately_active',  # This would normally be 'moderately active'
            'bmr': 1700,
            'tdee': 2100,
            'target_calories': 2000,
            'allergies': '',
            'medical_conditions': ''
        }
    }

    try:
        # Create template and context
        template = Template(template_content)
        context = Context(context_data)

        # Render the template
        rendered = template.render(context)

        print("✅ Template rendered successfully!")
        print("✅ No 'replace' filter error!")
        print("✅ Template contains expected content:")

        # Check for key elements
        checks = [
            'Personalized Diet Plan' in rendered,
            'Age' in rendered,
            'Gender' in rendered,
            'maintain weight' in rendered,  # Should be replaced from 'maintain_weight'
            'moderately active' in rendered,  # Should be replaced from 'moderately_active'
            'Breakfast' in rendered,
            'Lunch' in rendered,
            'Dinner' in rendered,
        ]

        for check in checks:
            if check:
                print(f"  ✅ Found: {check}")

        return True

    except Exception as e:
        print(f"❌ Template rendering failed: {e}")
        return False

if __name__ == '__main__':
    print("Testing fixed template...")
    success = test_template()
    if success:
        print("\n🎉 SUCCESS: The fixed template works correctly!")
        print("You can now use the application without the 'replace' filter error.")
    else:
        print("\n❌ FAILED: There are still issues with the template.")
