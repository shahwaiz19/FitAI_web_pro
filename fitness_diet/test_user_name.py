import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from fitness_diet.models import UserProfile

def test_user_name_display():
    print("=== TESTING USER NAME DISPLAY ===")

    # Test with a user that has a name
    user = UserProfile.objects.filter(name__isnull=False).exclude(name='').first()
    if user:
        print(f"Test user found: ID={user.id}, Name='{user.name}', Email={user.email}")
        print(f"Name length: {len(user.name)}")
        print(f"Name is empty: {user.name == ''}")
        print(f"Name is None: {user.name is None}")
    else:
        print("No user with name found!")

    # Check all users for empty names
    all_users = UserProfile.objects.all()
    print(f"\nChecking all {all_users.count()} users for empty names:")
    for u in all_users:
        if not u.name or u.name.strip() == '':
            print(f"User ID {u.id} has empty name! Email: {u.email}")

if __name__ == '__main__':
    test_user_name_display()
