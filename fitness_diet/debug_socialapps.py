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

def debug_socialapps():
    """Debug social apps configuration"""
    print("=== Social Apps Debug ===")

    # Get all social apps
    all_apps = SocialApp.objects.all()
    print(f"Total social apps: {all_apps.count()}")

    for app in all_apps:
        print(f"App ID: {app.id}, Name: {app.name}, Provider: {app.provider}")
        sites = app.sites.all()
        print(f"  Sites: {[f'{site.id}: {site.domain}' for site in sites]}")
        print(f"  Client ID: {app.client_id[:20]}...")
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

if __name__ == '__main__':
    debug_socialapps()
