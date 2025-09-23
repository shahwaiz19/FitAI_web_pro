import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from fitness_diet.models import UserProfile

def debug_session_issue():
    print("=== DEBUGGING SESSION ISSUE ===")

    # Check all users
    users = UserProfile.objects.all()
    print(f"\nTotal users in database: {users.count()}")

    for user in users:
        print(f"User ID: {user.id}, Name: '{user.name}', Email: {user.email}")

    print("\n=== POSSIBLE ISSUES ===")
    print("1. Session user_id might not match any user ID")
    print("2. User might be logging in with wrong credentials")
    print("3. Session might not be persisting correctly")
    print("4. User object might not be found due to DoesNotExist exception")

    print("\n=== RECOMMENDED FIXES ===")
    print("1. Check browser session/cookies")
    print("2. Try clearing browser cache and cookies")
    print("3. Verify login credentials match database")
    print("4. Check if user_id in session is valid")

if __name__ == '__main__':
    debug_session_issue()
