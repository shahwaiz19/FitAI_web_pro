import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_diet.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

def create_google_social_app():
    site = Site.objects.get_current()
    import json
    with open(r'c:/Users/shahw/Downloads/client_secret_1078564344145-er8a96v09dp59stl1632hurcvv4ubnco.apps.googleusercontent.com.json') as f:
        data = json.load(f)
    client_id = data['web']['client_id']
    client_secret = data['web']['client_secret']
    app, created = SocialApp.objects.get_or_create(
        provider='google',
        name='Google OAuth',
        client_id=client_id,
        secret=client_secret,
    )
    if created:
        app.sites.add(site)
        app.save()
        print("Google SocialApp created and linked to site.")
    else:
        print("Google SocialApp already exists.")

if __name__ == '__main__':
    create_google_social_app()
