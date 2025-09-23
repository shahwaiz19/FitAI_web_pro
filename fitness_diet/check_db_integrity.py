#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.db import connection

def check_db_integrity():
    print("=== Database Integrity Check ===")

    # Check SocialApp table
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM socialaccount_socialapp")
        socialapp_rows = cursor.fetchall()
        print(f"socialaccount_socialapp rows: {len(socialapp_rows)}")
        for row in socialapp_rows:
            print(f"  ID: {row[0]}, Provider: {row[1]}, Name: {row[3]}")

    # Check socialaccount_socialapp_sites table
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM socialaccount_socialapp_sites")
        sites_rows = cursor.fetchall()
        print(f"\nsocialaccount_socialapp_sites rows: {len(sites_rows)}")
        for row in sites_rows:
            print(f"  SocialApp ID: {row[1]}, Site ID: {row[2]}")

    # Check for duplicates
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT socialapp_id, site_id, COUNT(*)
            FROM socialaccount_socialapp_sites
            GROUP BY socialapp_id, site_id
            HAVING COUNT(*) > 1
        """)
        duplicates = cursor.fetchall()
        if duplicates:
            print(f"\n⚠️  Found duplicates in socialaccount_socialapp_sites: {duplicates}")
        else:
            print("\n✅ No duplicates found in socialaccount_socialapp_sites")

    # Check Django sites
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM django_site")
        site_rows = cursor.fetchall()
        print(f"\ndjango_site rows: {len(site_rows)}")
        for row in site_rows:
            print(f"  ID: {row[0]}, Domain: {row[1]}")

    # Test the exact query that allauth uses
    print("\n=== Testing Allauth Query ===")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT "socialaccount_socialapp"."id"
            FROM "socialaccount_socialapp"
            INNER JOIN "socialaccount_socialapp_sites"
            ON ("socialaccount_socialapp"."id" = "socialaccount_socialapp_sites"."socialapp_id")
            WHERE ("socialaccount_socialapp_sites"."site_id" = 2
            AND ("socialaccount_socialapp"."provider" = 'google'
            OR "socialaccount_socialapp"."provider_id" = 'google'))
        """)
        results = cursor.fetchall()
        print(f"Allauth query results: {len(results)} rows")
        for row in results:
            print(f"  SocialApp ID: {row[0]}")

if __name__ == '__main__':
    check_db_integrity()
