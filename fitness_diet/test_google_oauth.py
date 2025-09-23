import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def test_google_oauth_config():
    print("Testing Google OAuth Configuration...")

    # Check sites
    sites = Site.objects.all()
    print(f"Sites: {[site.name for site in sites]}")

    # Check social apps
    apps = SocialApp.objects.all()
    for app in apps:
        print(f"Social App: {app.name}, Provider: {app.provider}")
        print(f"Client ID: {app.client_id[:20]}...")
        print(f"Sites: {[site.name for site in app.sites.all()]}")

    # Check current site
    try:
        current_site = Site.objects.get_current()
        print(f"Current Site: {current_site.name} (ID: {current_site.id})")
    except Exception as e:
        print(f"Error getting current site: {e}")

if __name__ == '__main__':
    test_google_oauth_config()
