from django import template
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.urls import reverse

register = template.Library()

@register.simple_tag
def safe_provider_login_url(provider):
    """
    Safe version of provider_login_url that handles MultipleObjectsReturned
    """
    try:
        # Use the standard allauth URL pattern
        return reverse('socialaccount_login', kwargs={'provider': provider})
    except Exception as e:
        print(f"Error generating provider login URL: {e}")
        return '#'
