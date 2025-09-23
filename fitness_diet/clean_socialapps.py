#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')

django.setup()

from allauth.socialaccount.models import SocialApp

def clean_duplicate_socialapps():
    """Clean up duplicate social apps"""
    print("Checking for duplicate social apps...")

    # Get all Google social apps
    google_apps = SocialApp.objects.filter(provider='google')
    print(f"Found {google_apps.count()} Google social apps:")

    for app in google_apps:
        print(f"ID: {app.id}, Name: {app.name}, Client ID: {app.client_id[:20]}...")

    if google_apps.count() > 1:
        print("\nMultiple Google apps found. Keeping the first one and deleting others...")

        # Keep the first one, delete the rest
        apps_to_delete = google_apps[1:]
        for app in apps_to_delete:
            print(f"Deleting app ID: {app.id}")
            app.delete()

        print("Cleanup completed.")
    else:
        print("No duplicate Google apps found.")

if __name__ == '__main__':
    clean_duplicate_socialapps()
