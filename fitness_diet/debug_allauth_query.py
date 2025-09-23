#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.adapter import get_adapter
from django.test import RequestFactory
from django.db import connection
from django.conf import settings

def debug_allauth_query():
    print("=== Debugging Allauth Query ===")

    # Enable query logging
    from django.db import connection
    from django.conf import settings
    settings.DEBUG = True

    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/login/')

    # Get the adapter
    adapter = get_adapter()

    # Log queries
    print("Executing adapter.get_app()...")
    queries_before = len(connection.queries)

    try:
        app = adapter.get_app(request, provider='google')
        print(f"Success: {app}")
    except Exception as e:
        print(f"Error: {e}")
        queries_after = len(connection.queries)
        print(f"Queries executed: {queries_after - queries_before}")

        # Show the last few queries
        for i in range(max(0, queries_after - 3), queries_after):
            if i < len(connection.queries):
                query = connection.queries[i]
                print(f"Query {i}: {query['sql']}")

    # Also check what the raw query would be
    print("\n=== Manual Query Check ===")
    try:
        apps = SocialApp.objects.filter(provider='google', sites__id=settings.SITE_ID)
        print(f"Manual query result count: {apps.count()}")
        for app in apps:
            print(f"App: {app.id} - {app.name}")
    except Exception as e:
        print(f"Manual query error: {e}")

if __name__ == '__main__':
    debug_allauth_query()
