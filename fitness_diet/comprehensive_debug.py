#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')

django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

def comprehensive_debug():
    """Comprehensive debug of social apps and allauth configuration"""
    print("=== Comprehensive Social Apps Debug ===")

    # Get all social apps
    all_apps = SocialApp.objects.all()
    print(f"Total social apps: {all_apps.count()}")

    for app in all_apps:
        print(f"App ID: {app.id}, Name: {app.name}, Provider: {app.provider}")
        sites = app.sites.all()
        print(f"  Sites: {[f'{site.id}: {site.domain}' for site in sites]}")
        print(f"  Client ID: {app.client_id[:20]}...")
        print(f"  Secret: {'*' * len(app.secret) if app.secret else 'None'}")
        print()

    # Get Google apps specifically
    google_apps = SocialApp.objects.filter(provider='google')
    print(f"Google apps: {google_apps.count()}")

    # Get current site
    try:
        current_site = Site.objects.get_current()
        print(f"Current site: {current_site.id}: {current_site.domain}")
    except Exception as e:
        print(f"Error getting current site: {e}")

    # Check sites
    sites = Site.objects.all()
    print(f"All sites: {[(site.id, site.domain) for site in sites]}")

    # Try to simulate the allauth adapter get_app method
    print("\n=== Testing allauth adapter ===")
    adapter = DefaultSocialAccountAdapter()

    try:
        # This is what the template tag does
        from django.contrib.sites.models import Site
        current_site = Site.objects.get_current()
        google_app = SocialApp.objects.get(provider='google', sites=current_site)
        print(f"Successfully found Google app for current site: {google_app.name}")
    except SocialApp.DoesNotExist:
        print("No Google app found for current site")
    except SocialApp.MultipleObjectsReturned:
        print("Multiple Google apps found for current site - this is the issue!")
        apps = SocialApp.objects.filter(provider='google', sites=current_site)
        for app in apps:
            print(f"  Duplicate app: {app.id} - {app.name}")
    except Exception as e:
        print(f"Error in adapter test: {e}")

if __name__ == '__main__':
    comprehensive_debug()
