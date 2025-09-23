#!/usr/bin/env python
import os
import sys
import django
import json

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')

django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def update_google_socialapp():
    # Load credentials from JSON file
    json_path = r'c:/Users/shahw/Downloads/client_secret_1078564344145-er8a96v09dp59stl1632hurcvv4ubnco.apps.googleusercontent.com.json'

    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            client_id = data['web']['client_id']
            client_secret = data['web']['client_secret']
    except FileNotFoundError:
        print("JSON file not found. Using placeholder values.")
        client_id = "1078564344145-er8a96v09dp59stl1632hurcvv4ubnco.apps.googleusercontent.com"
        client_secret = "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"

    # Get or create the Google SocialApp
    google_app, created = SocialApp.objects.get_or_create(
        provider='google',
        defaults={'name': 'Google OAuth'}
    )

    # Update credentials
    google_app.client_id = client_id
    google_app.secret = client_secret
    google_app.save()

    # Update sites
    site1, _ = Site.objects.get_or_create(
        domain='localhost:8000',
        defaults={'name': 'localhost'}
    )
    site2, _ = Site.objects.get_or_create(
        domain='127.0.0.1:8000',
        defaults={'name': 'localhost'}
    )
    google_app.sites.set([site1, site2])
    google_app.save()

    print(f"Updated Google SocialApp:")
    print(f"  Name: {google_app.name}")
    print(f"  Client ID: {google_app.client_id}")
    print(f"  Sites: {[s.domain for s in google_app.sites.all()]}")

if __name__ == '__main__':
    update_google_socialapp()
