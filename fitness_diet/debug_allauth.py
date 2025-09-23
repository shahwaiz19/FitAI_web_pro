#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from allauth.socialaccount.adapter import get_adapter
from django.test import RequestFactory
from django.contrib.sites.models import Site

def debug_allauth():
    print("=== Debugging Allauth Adapter ===")

    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/login/')

    # Get the adapter
    adapter = get_adapter()
    print(f"Adapter: {adapter}")

    try:
        # Try to get the Google provider
        provider = adapter.get_provider(request, 'google')
        print(f"Provider: {provider}")
    except Exception as e:
        print(f"Error getting provider: {e}")

    try:
        # Try to get the app
        app = adapter.get_app(request, provider='google')
        print(f"App: {app}")
    except Exception as e:
        print(f"Error getting app: {e}")
        import traceback
        traceback.print_exc()

    # Check current site
    current_site = Site.objects.get_current()
    print(f"Current site: {current_site} (ID: {current_site.id})")

    # Check SITE_ID setting
    from django.conf import settings
    print(f"SITE_ID setting: {getattr(settings, 'SITE_ID', 'Not set')}")

if __name__ == '__main__':
    debug_allauth()
