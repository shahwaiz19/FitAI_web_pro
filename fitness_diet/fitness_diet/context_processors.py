from .models import UserProfile
from django.conf import settings
import time

def branding_context(request):
    """
    Context processor for consistent branding across all templates.
    Provides brand name, logo, and user profile information.
    Handles edge cases like cached images and authentication states.
    """
    # Brand configuration
    brand_config = {
        'brand_name': 'FitAI',
        'brand_logo_svg': '''
        <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
            <path d="M36.7273 44C33.9891 44 31.6043 39.8386 30.3636 33.69C29.123 39.8386 26.7382 44 24 44C21.2618 44 18.877 39.8386 17.6364 33.69C16.3957 39.8386 14.0109 44 11.2727 44C7.25611 44 4 35.0457 4 24C4 12.9543 7.25611 4 11.2727 4C14.0109 4 16.3957 8.16144 17.6364 14.31C18.877 8.16144 21.2618 4 24 4C26.7382 4 29.123 8.16144 30.3636 14.31C31.6043 8.16144 33.9891 4 36.7273 4C40.7439 4 44 12.9543 44 24C44 35.0457 40.7439 44 36.7273 44Z" fill="currentColor"/>
        </svg>
        ''',
        'brand_icon_class': 'fas fa-dumbbell',
        'primary_color': '#11d452',
        'secondary_color': '#0d1b12',
    }

    # User profile information with edge case handling
    user_profile = None
    user_profile_pic_url = None
    cache_buster = None

    if request.user.is_authenticated:
        # Try to get UserProfile first (our custom auth system)
        if hasattr(request, 'session') and 'user_id' in request.session:
            try:
                user_profile = UserProfile.objects.select_related().get(id=request.session['user_id'])
                if user_profile.profile_picture and user_profile.profile_picture.name:
                    # Add cache busting parameter to prevent cached images
                    cache_buster = int(time.time()) if settings.DEBUG else user_profile.profile_picture.size
                    user_profile_pic_url = f"{user_profile.profile_picture.url}?v={cache_buster}"
                else:
                    # Fallback to social account avatar
                    social_accounts = request.user.socialaccount_set.all()
                    if social_accounts.exists():
                        social_account = social_accounts.first()
                        user_profile_pic_url = social_account.get_avatar_url()
            except (UserProfile.DoesNotExist, AttributeError):
                # Handle case where user_id in session doesn't match any UserProfile
                pass
        else:
            # Fallback to social account avatar for allauth-only users
            try:
                social_accounts = request.user.socialaccount_set.all()
                if social_accounts.exists():
                    social_account = social_accounts.first()
                    user_profile_pic_url = social_account.get_avatar_url()
            except AttributeError:
                # Handle case where socialaccount app is not properly configured
                pass

    # Default avatar if no profile picture found
    if not user_profile_pic_url:
        user_profile_pic_url = f"{settings.STATIC_URL}images/default-avatar.svg"

    # Additional context for edge cases
    context = {
        'brand': brand_config,
        'user_profile': user_profile,
        'user_profile_pic_url': user_profile_pic_url,
        'is_authenticated': request.user.is_authenticated,
        'user_display_name': user_profile.name if user_profile else (request.user.get_full_name() or request.user.username if request.user.is_authenticated else ''),
        'cache_buster': cache_buster,
        'debug_mode': settings.DEBUG,
    }

    return context