import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from fitness_diet.models import UserProfile

print('Matching check between SocialAccount emails and UserProfile emails:')
for sa in SocialAccount.objects.filter(provider='google'):
    has_profile = UserProfile.objects.filter(email=sa.user.email).exists()
    status = 'YES' if has_profile else 'NO'
    print(f'  {sa.user.email} -> UserProfile: {status}')

print('\nAll UserProfile emails:')
for up in UserProfile.objects.all():
    print(f'  {up.email}')

print('\nAll SocialAccount emails:')
for sa in SocialAccount.objects.filter(provider='google'):
    print(f'  {sa.user.email}')
