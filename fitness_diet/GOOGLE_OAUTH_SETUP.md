# Google OAuth Setup for Django Project

This guide will help you set up Google OAuth credentials and configure your Django project to fix the 400 error during OAuth login.

## Step 1: Create OAuth Credentials in Google Cloud Console

1. Go to the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
2. Select your project or create a new one.
3. Navigate to **APIs & Services > Credentials**.
4. Click **Create Credentials > OAuth client ID**.
5. Configure the consent screen if prompted.
6. Choose **Web application** as the application type.
7. Set the **Authorized redirect URIs** to:
   - `http://localhost:8000/accounts/google/login/callback/`
   - (Add any other URLs your app uses for OAuth callbacks)
8. Click **Create** and note the **Client ID** and **Client Secret**.

## Step 2: Configure Django Settings

1. Open your Django settings file (`settings.py`).
2. Add or update the following with your credentials:

```python
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '<YOUR_CLIENT_ID>',
            'secret': '<YOUR_CLIENT_SECRET>',
            'key': ''
        }
    }
}
```

3. Ensure your `INSTALLED_APPS` includes:

```python
INSTALLED_APPS = [
    # ...
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # ...
]

SITE_ID = 1
```

## Step 3: Verify URLs

Make sure your `urls.py` includes:

```python
path('accounts/', include('allauth.urls')),
```

## Step 4: Restart Server and Test

1. Restart your Django development server.
2. Navigate to the login page and try signing in with Google.
3. If you still get errors, check the console logs and ensure redirect URIs match exactly.

---

If you want, I can help you update your `settings.py` and `urls.py` files with the correct configuration. Please confirm.
