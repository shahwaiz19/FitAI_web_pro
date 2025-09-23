#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def check_socialapps():
    print("=== SocialApp Analysis ===")

    # Get all SocialApps
    all_apps = SocialApp.objects.all()
    print(f"Total SocialApps: {all_apps.count()}")

    for app in all_apps:
        sites = list(app.sites.all())
        print(f"ID: {app.id}, Provider: {app.provider}, Name: {app.name}")
        print(f"  Sites: {[f'{s.id}:{s.domain}' for s in sites]}")
        if len(sites) > 1:
            print(f"  ⚠️  Multiple sites for app {app.id}")

    print("\n=== Site Analysis ===")
    sites = Site.objects.all()
    for site in sites:
        print(f"ID: {site.id}, Domain: {site.domain}")

    print("\n=== Google Apps Analysis ===")
    google_apps = SocialApp.objects.filter(provider='google')
    print(f"Google apps count: {google_apps.count()}")

    for app in google_apps:
        print(f"Google App ID: {app.id}, Sites: {[s.id for s in app.sites.all()]}")

    # Check if there are multiple apps for the same provider/site combination
    print("\n=== Checking for duplicates ===")
    providers = SocialApp.objects.values_list('provider', flat=True).distinct()
    for provider in providers:
        apps = SocialApp.objects.filter(provider=provider)
        if apps.count() > 1:
            print(f"⚠️  Multiple apps for provider '{provider}': {apps.count()}")

if __name__ == '__main__':
    check_socialapps()
