from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.core.exceptions import MultipleObjectsReturned

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter that handles MultipleObjectsReturned exceptions
    """

    def get_app(self, request, provider, **kwargs):
        """
        Override get_app to handle MultipleObjectsReturned gracefully
        """
        try:
            return super().get_app(request, provider, **kwargs)
        except MultipleObjectsReturned:
            # If multiple apps found, get the first one for the current site
            current_site = Site.objects.get_current()
            apps = SocialApp.objects.filter(provider=provider, sites=current_site)
            if apps.exists():
                return apps.first()
            else:
                # Fallback to any app for this provider
                apps = SocialApp.objects.filter(provider=provider)
                if apps.exists():
                    return apps.first()
                else:
                    raise SocialApp.DoesNotExist(f"No social app found for provider {provider}")
