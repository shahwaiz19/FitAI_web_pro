from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OnboardingWelcomeForm, OnboardingGoalForm, OnboardingInfoForm, OnboardingAccountForm
from .models import UserProfile
from django.contrib.auth.hashers import make_password, check_password
from allauth.socialaccount.models import SocialAccount
from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
import requests
from PIL import Image
from io import BytesIO
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from transformers import pipeline
import torch
import os

def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

API_KEY = os.environ.get('USDA_API_KEY', '')

def landing_page(request):
    if request.method == 'POST':
        # Handle workout generator form submission
        age = int(request.POST.get('age'))
        weight = float(request.POST.get('weight'))
        height = float(request.POST.get('height'))
        goal = request.POST.get('goal')

        # Import and use the workout model
        import joblib
        import os
        from django.conf import settings

        MODEL_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'workout_plan', 'workout_suggestion_generator.pkl')
        try:
            workout_model = joblib.load(MODEL_PATH)
            features = [[age, weight, height]]
            prediction = workout_model.predict(features)[0]
        except Exception as e:
            prediction = "Mixed cardio and strength training"

        return render(request, 'landing.html', {'prediction': prediction})

    return render(request, 'landing.html')

def login_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')  # Can be email or username
        password = request.POST.get('password')

        # Try to find user by email first
        user = UserProfile.objects.filter(email=login).first()

        if user and check_password(password, user.password):
            # Store user info in session
            request.session['user_id'] = user.id
            request.session['user_name'] = user.name
            request.session['user_email'] = user.email
            request.session['user_goal'] = user.goal

            messages.success(request, f'Welcome back, {user.name}!')

            # Redirect based on goal
            if user.goal == 'gain_weight':
                return redirect('gain_weight_plan')
            elif user.goal == 'lose_weight':
                return redirect('lose_weight_plan')
            elif user.goal == 'maintain_weight':
                return redirect('landing')
            else:
                return redirect('landing')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')

def onboarding_welcome(request):
    if request.method == 'POST':
        form = OnboardingWelcomeForm(request.POST)
        if form.is_valid():
            request.session['name'] = form.cleaned_data['name']
            return redirect('onboarding_goal')
    else:
        form = OnboardingWelcomeForm()
    return render(request, 'onboarding_welcome.html', {'form': form})

def onboarding_goal(request):
    if 'name' not in request.session:
        return redirect('onboarding_welcome')
    if request.method == 'POST':
        form = OnboardingGoalForm(request.POST)
        if form.is_valid():
            request.session['goal'] = form.cleaned_data['goal']
            return redirect('onboarding_info')
    else:
        form = OnboardingGoalForm()
    return render(request, 'onboarding_goal.html', {'form': form})

def onboarding_info(request):
    if 'goal' not in request.session:
        return redirect('onboarding_goal')
    if request.method == 'POST':
        form = OnboardingInfoForm(request.POST)
        if form.is_valid():
            request.session['age'] = form.cleaned_data['age']
            request.session['sex'] = form.cleaned_data['sex']
            request.session['height'] = form.cleaned_data['height']
            request.session['weight'] = form.cleaned_data['weight']
            request.session['weekly_goal'] = form.cleaned_data['weekly_goal']
            return redirect('onboarding_account')
    else:
        form = OnboardingInfoForm()
    return render(request, 'onboarding_info.html', {'form': form})

def onboarding_account(request):
    if 'weekly_goal' not in request.session:
        return redirect('onboarding_info')
    if request.method == 'POST':
        form = OnboardingAccountForm(request.POST)
        if form.is_valid():
            # Check if user with email already exists
            email = form.cleaned_data['email']
            existing_user = UserProfile.objects.filter(email=email).first()
            if existing_user:
                messages.error(request, 'An account with this email already exists.')
                return render(request, 'onboarding_account.html', {'form': form})
            # Save to database
            user_profile = UserProfile.objects.create(
                name=request.session['name'],
                goal=request.session['goal'],
                age=request.session['age'],
                sex=request.session['sex'],
                height=request.session['height'],
                weight=request.session['weight'],
                weekly_goal=request.session['weekly_goal'],
                email=email,
                password=make_password(form.cleaned_data['password'])
            )
            # Clear onboarding session data
            for key in ['name', 'goal', 'age', 'sex', 'height', 'weight', 'weekly_goal']:
                if key in request.session:
                    del request.session[key]

            # Set user session for immediate login after account creation
            request.session['user_id'] = user_profile.id
            request.session['user_name'] = user_profile.name
            request.session['user_email'] = user_profile.email
            request.session['user_goal'] = user_profile.goal

            messages.success(request, 'Account created successfully!')
            # Redirect based on goal
            if user_profile.goal == 'gain_weight':
                return redirect('gain_weight_plan')
            elif user_profile.goal == 'lose_weight':
                return redirect('lose_weight_plan')
            elif user_profile.goal == 'maintain_weight':
                # TODO: Add maintain weight plan page and URL
                return redirect('landing')
            else:
                return redirect('landing')
    else:
        form = OnboardingAccountForm()
    return render(request, 'onboarding_account.html', {'form': form})

@receiver(user_signed_up)
def handle_google_signup(sender, request, user, **kwargs):
    """Handle Google OAuth signup and save user profile data"""
    if 'weekly_goal' in request.session:
        # Check if user with email already exists
        existing_user = UserProfile.objects.filter(email=user.email).first()
        if existing_user:
            messages.error(request, 'An account with this email already exists.')
            return
        # User has completed onboarding, save their data
        user_profile = UserProfile.objects.create(
            name=request.session.get('name', user.first_name or 'User'),
            goal=request.session['goal'],
            age=request.session['age'],
            sex=request.session['sex'],
            height=request.session['height'],
            weight=request.session['weight'],
            weekly_goal=request.session['weekly_goal'],
            email=user.email,
            password=''  # No password for OAuth users
        )
        # Clear session
        for key in ['name', 'goal', 'age', 'sex', 'height', 'weight', 'weekly_goal']:
            if key in request.session:
                del request.session[key]
        messages.success(request, 'Account created successfully with Google!')

        # Store user info in session for immediate login
        request.session['user_id'] = user_profile.id
        request.session['user_name'] = user_profile.name
        request.session['user_email'] = user_profile.email
        request.session['user_goal'] = user_profile.goal

@receiver(user_logged_in)
def handle_google_login(sender, request, user, **kwargs):
    """Handle Google OAuth login for existing users"""
    # Check if this is a social login
    if hasattr(user, 'socialaccount_set') and user.socialaccount_set.exists():
        # Try to find existing UserProfile
        user_profile = UserProfile.objects.filter(email=user.email).first()

        if user_profile:
            # Store user info in session
            request.session['user_id'] = user_profile.id
            request.session['user_name'] = user_profile.name
            request.session['user_email'] = user_profile.email
            request.session['user_goal'] = user_profile.goal

            messages.success(request, f'Welcome back, {user_profile.name}!')
        else:
            # User doesn't have a profile yet, redirect to onboarding
            messages.info(request, 'Please complete your profile setup.')

def gain_weight_plan(request):
    user = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            user = None
    return render(request, 'gain_weight_plan.html', {'user': user})

def lose_weight_plan(request):
    user = None
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            user = None
    return render(request, 'lose_weight_plan.html', {'user': user})

@csrf_exempt
def food_recognition_page(request):
    if request.method == 'POST' and request.FILES.get('food_image'):
        try:
            uploaded_file = request.FILES['food_image']
            image = Image.open(uploaded_file)

            # Load model with GPU if available
            device = 0 if torch.cuda.is_available() else -1
            classifier = pipeline('image-classification', model='nateraw/food', device=device)

            preds = classifier(image, top_k=1)
            food_label = preds[0]['label']

            # Fetch nutritional data from USDA API
            url = f'https://api.nal.usda.gov/fdc/v1/foods/search?query={food_label}&api_key={API_KEY}'
            response = requests.get(url)
            data = response.json()

            # Default nutritional values
            calories = 'Not found'
            protein = 'Not found'
            carbs = 'Not found'
            fat = 'Not found'

            if 'foods' in data and len(data['foods']) > 0:
                food = data['foods'][0]
                for nutrient in food.get('foodNutrients', []):
                    nutrient_name = nutrient.get('nutrientName', '')
                    if 'Energy' in nutrient_name and 'kcal' in nutrient.get('unitName', '').lower():
                        calories = f"{nutrient['value']} kcal"
                    elif 'Protein' in nutrient_name:
                        protein = f"{nutrient['value']}g"
                    elif 'Carbohydrate' in nutrient_name:
                        carbs = f"{nutrient['value']}g"
                    elif 'Total lipid' in nutrient_name or 'Fat' in nutrient_name:
                        fat = f"{nutrient['value']}g"

            # Calculate health score (simple algorithm)
            health_score = 7.5  # Default score
            if calories != 'Not found':
                try:
                    cal_value = float(calories.split()[0])
                    if cal_value < 200:
                        health_score = 8.5
                    elif cal_value < 400:
                        health_score = 7.5
                    elif cal_value < 600:
                        health_score = 6.0
                    else:
                        health_score = 4.5
                except:
                    pass

            return JsonResponse({
                'food_name': food_label.title(),
                'calories': calories,
                'protein': protein,
                'carbs': carbs,
                'fat': fat,
                'confidence': f"{preds[0]['score']:.1%}",
                'health_score': health_score
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'food_recognition.html')
