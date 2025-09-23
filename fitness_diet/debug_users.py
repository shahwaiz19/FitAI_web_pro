import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from fitness_diet.models import UserProfile

def check_users():
    users = UserProfile.objects.all()
    print(f'Total users: {users.count()}')
    for user in users:
        print(f'ID: {user.id}, Name: "{user.name}", Email: {user.email}, Goal: {user.goal}')

if __name__ == '__main__':
    check_users()
