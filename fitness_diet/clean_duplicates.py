import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from fitness_diet.models import UserProfile

def clean_duplicate_users():
    """Clean duplicate UserProfile entries based on email, keeping the most recent one."""
    from django.db.models import Count

    # Find emails with multiple profiles
    duplicates = UserProfile.objects.values('email').annotate(count=Count('id')).filter(count__gt=1)

    print(f"Found {len(duplicates)} emails with duplicates")

    for dup in duplicates:
        email = dup['email']
        profiles = UserProfile.objects.filter(email=email).order_by('-created_at')

        # Keep the most recent one
        keep_profile = profiles.first()
        delete_profiles = profiles[1:]

        print(f"Email: {email}")
        print(f"  Keeping: {keep_profile.name} (created: {keep_profile.created_at})")
        print(f"  Deleting {len(delete_profiles)} duplicates:")

        for profile in delete_profiles:
            print(f"    - {profile.name} (created: {profile.created_at})")
            profile.delete()

        print()

    print("Duplicate cleanup completed.")

if __name__ == '__main__':
    clean_duplicate_users()
