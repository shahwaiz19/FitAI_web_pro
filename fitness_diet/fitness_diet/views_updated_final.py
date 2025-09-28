from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from .forms import OnboardingWelcomeForm, OnboardingGoalForm, OnboardingInfoForm, OnboardingAccountForm
from .models import UserProfile, DietPlan, WorkoutPlan, WeightPrediction, CalorieCalculation, FoodRecognition, HealthAssessment
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
import joblib
import os
import numpy as np
from django.conf import settings

API_KEY = "USE YOUR OWN API " // YHOU WILL GET IT FROM usda food data center

def landing_page(request):
    # Check if there's a pending redirect from OAuth login
    redirect_url = request.session.pop('redirect_after_login', None)
    if redirect_url:
        return redirect(redirect_url)
    return render(request, 'landing.html')

from django.core.exceptions import MultipleObjectsReturned

def login_view(request):
    from django.contrib.auth import authenticate, login as django_login
    from django.contrib.auth.models import User
    
    if request.method == 'POST':
        login = request.POST.get('login')  # Can be email or username
        password = request.POST.get('password')

        try:
            # Try to find user by email first
            user_profile = UserProfile.objects.get(email=login)
        except UserProfile.DoesNotExist:
            messages.error(request, 'User not found with the provided email.')
            return render(request, 'login.html')
        except MultipleObjectsReturned:
            messages.error(request, 'Multiple accounts found with this email. Please contact support.')
            return render(request, 'login.html')

        if check_password(password, user_profile.password):
            # Try to find or create corresponding Django User
            try:
                django_user = User.objects.get(email=login)
            except User.DoesNotExist:
                # Create Django User for this UserProfile
                django_user = User.objects.create_user(
                    username=login,
                    email=login,
                    first_name=user_profile.name.split()[0] if user_profile.name else '',
                    last_name=' '.join(user_profile.name.split()[1:]) if user_profile.name and len(user_profile.name.split()) > 1 else ''
                )
                django_user.set_password(password)
                django_user.save()
            
            # Authenticate and login with Django's system
            django_user = authenticate(request, username=login, password=password)
            if django_user:
                django_login(request, django_user)
            
            # Store user info in session
            request.session['user_id'] = user_profile.id
            request.session['user_name'] = user_profile.name
            request.session['user_email'] = user_profile.email
            request.session['user_goal'] = user_profile.goal

            messages.success(request, f'Welcome back, {user_profile.name}!')

            # Redirect to dashboard instead of goal-specific pages
            return redirect('dashboard')
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
    required_keys = ['name', 'goal', 'age', 'sex', 'height', 'weight', 'weekly_goal']
    for key in required_keys:
        if key not in request.session:
            return redirect('onboarding_welcome')
    if request.method == 'POST':
        form = OnboardingAccountForm(request.POST)
        if form.is_valid():
            # Check if user with email already exists
            email = form.cleaned_data['email']
            try:
                existing_user = UserProfile.objects.get(email=email)
                messages.error(request, 'An account with this email already exists.')
                return render(request, 'onboarding_account.html', {'form': form})
            except UserProfile.DoesNotExist:
                pass  # Good, no existing user
            except UserProfile.MultipleObjectsReturned:
                messages.error(request, 'Multiple accounts found with this email. Please contact support.')
                return render(request, 'onboarding_account.html', {'form': form})

            # Save to database
            try:
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
            except Exception as e:
                print(f"Error creating user profile: {e}")
                messages.error(request, 'An error occurred while creating your account. Please try again.')
                return render(request, 'onboarding_account.html', {'form': form})

            # Create Django User and log in
            from django.contrib.auth.models import User
            from django.contrib.auth import authenticate, login as django_login

            try:
                django_user = User.objects.get(email=user_profile.email)
            except User.DoesNotExist:
                django_user = User.objects.create_user(
                    username=user_profile.email,
                    email=user_profile.email,
                    first_name=user_profile.name.split()[0] if user_profile.name else '',
                    last_name=' '.join(user_profile.name.split()[1:]) if user_profile.name and len(user_profile.name.split()) > 1 else ''
                )
                django_user.set_password(form.cleaned_data['password'])
                django_user.save()

            django_user = authenticate(request, username=user_profile.email, password=form.cleaned_data['password'])
            if django_user:
                django_login(request, django_user)

            # Clear session
            for key in ['name', 'goal', 'age', 'sex', 'height', 'weight', 'weekly_goal']:
                request.session.pop(key, None)
            messages.success(request, 'Account created successfully!')
            # Redirect based on goal
            if user_profile.goal == 'gain_weight':
                return redirect('gain_weight_plan')
            elif user_profile.goal == 'lose_weight':
                return redirect('lose_weight_plan')
            elif user_profile.goal == 'maintain_weight':
                return redirect('maintain_weight_plan')
            else:
                return redirect('landing')
    else:
        form = OnboardingAccountForm()
    return render(request, 'onboarding_account.html', {'form': form})

@receiver(user_signed_up)
def handle_google_signup(sender, request, user, **kwargs):
    """Handle Google OAuth signup and save user profile data"""
    print(f"Google signup triggered for user: {user.email}")  # Debug log

    if 'weekly_goal' in request.session or 'goal' in request.session:
        print("User has completed onboarding, creating profile...")  # Debug log

        # Check if user with email already exists
        try:
            existing_user = UserProfile.objects.get(email=user.email)
            messages.error(request, 'An account with this email already exists.')
            return
        except UserProfile.DoesNotExist:
            pass  # Good, no existing user
        except UserProfile.MultipleObjectsReturned:
            messages.error(request, 'Multiple accounts found with this email. Please contact support.')
            return

        # User has completed onboarding, save their data
        # Check if it's simplified onboarding (only name and goal) or full onboarding
        if 'weekly_goal' in request.session:
            # Full onboarding
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
            session_keys = ['name', 'goal', 'age', 'sex', 'height', 'weight', 'weekly_goal']
        else:
            # Simplified onboarding (only name and goal)
            user_profile = UserProfile.objects.create(
                name=request.session.get('name', user.first_name or 'User'),
                goal=request.session['goal'],
                email=user.email,
                password=''  # No password for OAuth users
            )
            # Clear session
            session_keys = ['name', 'goal']

        for key in session_keys:
            if key in request.session:
                del request.session[key]
        messages.success(request, 'Account created successfully with Google!')

        # Store user info in session for immediate login
        request.session['user_id'] = user_profile.id
        request.session['user_name'] = user_profile.name
        request.session['user_email'] = user_profile.email
        request.session['user_goal'] = user_profile.goal

        # Set redirect for after allauth login
        if user_profile.goal == 'gain_weight':
            request.session['redirect_after_login'] = 'gain_weight_plan'
        elif user_profile.goal == 'lose_weight':
            request.session['redirect_after_login'] = 'lose_weight_plan'
        elif user_profile.goal == 'maintain_weight':
            request.session['redirect_after_login'] = 'maintain_weight_plan'
        else:
            request.session['redirect_after_login'] = 'landing'
    else:
        print("User hasn't completed onboarding, redirecting to landing...")  # Debug log
        # User signed up but hasn't completed onboarding, redirect to landing page
        from django.shortcuts import redirect
        return redirect('landing')

@receiver(user_logged_in)
def handle_google_login(sender, request, user, **kwargs):
    """Handle Google OAuth login for existing users"""
    print(f"Google login triggered for user: {user.email}")  # Debug log

    # Check if this is a social login
    if hasattr(user, 'socialaccount_set') and user.socialaccount_set.exists():
        # Try to find existing UserProfile
        try:
            user_profile = UserProfile.objects.get(email=user.email)
            print(f"Found existing profile for {user.email}")  # Debug log
        except UserProfile.DoesNotExist:
            print(f"No profile found for {user.email}")  # Debug log
            # Check if user is in onboarding flow (has 'goal' in session)
            if 'goal' in request.session and 'name' in request.session:
                print("User is in onboarding flow, creating profile...")  # Debug log
                # Create profile for user in onboarding
                user_profile = UserProfile.objects.create(
                    name=request.session.get('name', user.first_name or 'User'),
                    goal=request.session['goal'],
                    email=user.email,
                    password=''  # No password for OAuth users
                )
                # Clear session
                for key in ['name', 'goal']:
                    if key in request.session:
                        del request.session[key]
                messages.success(request, 'Account created successfully with Google!')

                # Set redirect for after allauth login
                if user_profile.goal == 'gain_weight':
                    request.session['redirect_after_login'] = 'gain_weight_plan'
                elif user_profile.goal == 'lose_weight':
                    request.session['redirect_after_login'] = 'lose_weight_plan'
                elif user_profile.goal == 'maintain_weight':
                    request.session['redirect_after_login'] = 'maintain_weight_plan'
                else:
                    request.session['redirect_after_login'] = 'landing'
            else:
                print("User not in onboarding flow, redirecting to landing")  # Debug log
                # User doesn't have a profile yet, redirect to landing page
                messages.info(request, 'Please complete your profile setup.')
                from django.shortcuts import redirect
                return redirect('landing')
        except UserProfile.MultipleObjectsReturned:
            messages.error(request, 'Multiple accounts found with this email. Please contact support.')
            return

        # Store user info in session
        request.session['user_id'] = user_profile.id
        request.session['user_name'] = user_profile.name
        request.session['user_email'] = user_profile.email
        request.session['user_goal'] = user_profile.goal

        messages.success(request, f'Welcome back, {user_profile.name}!')

        # Set redirect for after allauth login
        if user_profile.goal == 'gain_weight':
            request.session['redirect_after_login'] = 'gain_weight_plan'
        elif user_profile.goal == 'lose_weight':
            request.session['redirect_after_login'] = 'lose_weight_plan'
        elif user_profile.goal == 'maintain_weight':
            request.session['redirect_after_login'] = 'maintain_weight_plan'
        else:
            request.session['redirect_after_login'] = 'landing'

def gain_weight_plan(request):
    # Check if user is logged in
    if not request.user.is_authenticated or 'user_id' not in request.session:
        messages.warning(request, 'Please log in to access your personalized plan.')
        return redirect('login')
    return render(request, 'gain_weight_plan.html')

def lose_weight_plan(request):
    # Check if user is logged in
    if not request.user.is_authenticated or 'user_id' not in request.session:
        messages.warning(request, 'Please log in to access your personalized plan.')
        return redirect('login')
    return render(request, 'lose_weight_plan.html')

def maintain_weight_plan(request):
    # Check if user is logged in
    if not request.user.is_authenticated or 'user_id' not in request.session:
        messages.warning(request, 'Please log in to access your personalized plan.')
        return redirect('login')
    return render(request, 'maintain_weight_plan.html')

def dashboard(request):
    # Check if user is logged in - require BOTH Django auth AND our session AND valid UserProfile
    if not request.user.is_authenticated or 'user_id' not in request.session:
        messages.warning(request, 'Please log in to access your dashboard.')
        return redirect('login')

    # Additional check: ensure UserProfile exists
    try:
        user_profile = UserProfile.objects.get(id=request.session['user_id'])
    except UserProfile.DoesNotExist:
        messages.warning(request, 'User profile not found. Please log in again.')
        return redirect('login')

    return render(request, 'dashboard.html')

def predict_weight_change(request):
    if request.method == 'POST':
        try:
            # Get form data - matching the 5 features expected by the model
            age = int(request.POST.get('age', 25))
            gender = request.POST.get('gender', 'male')
            current_weight = float(request.POST.get('current_weight', 70))  # Already in kg
            target_weight = float(request.POST.get('target_weight', 65))
            duration_weeks = int(request.POST.get('duration_weeks', 8))
            physical_activity_level = request.POST.get('physical_activity_level', 'moderately_active')

            # Calculate daily caloric surplus/deficit based on weight goals
            weight_difference_kg = target_weight - current_weight
            total_calories_needed = weight_difference_kg * 7700  # 7700 calories per kg
            daily_caloric_surplus_deficit = total_calories_needed / (duration_weeks * 7)

            # Load the model
            model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'weight_change', 'weight_change_model.pkl')
            model_dict = joblib.load(model_path)
            model = model_dict['model']
            scaler = model_dict.get('scaler')

            # Encode categorical variables (matching model expectations)
            gender_encoded = 1 if gender.lower() == 'male' else 0

            activity_map = {
                'sedentary': 0,
                'lightly_active': 1,
                'moderately_active': 2,
                'very_active': 3,
                'extremely_active': 4
            }
            physical_activity_encoded = activity_map.get(physical_activity_level, 2)

            # Prepare features for prediction (matching the 5 features expected by model)
            features = np.array([[
                age,
                gender_encoded,
                current_weight,
                daily_caloric_surplus_deficit,
                physical_activity_encoded
            ]])

            # Scale features if scaler exists
            if scaler:
                try:
                    features_scaled = scaler.transform(features)
                except Exception as scale_error:
                    print(f"Scaler transform failed: {scale_error}, using unscaled features")
                    features_scaled = features
            else:
                features_scaled = features

            # Make prediction - model returns [weight_change, duration]
            prediction = model.predict(features_scaled)[0]
            predicted_weight_change_kg = float(prediction[0])  # First output is weight change

            # Calculate additional metrics for display
            weekly_change_needed = weight_difference_kg / duration_weeks
            daily_calorie_adjustment = weekly_change_needed * 7700 / 7  # 7700 calories per kg

            # Save the weight prediction to database
            try:
                WeightPrediction.objects.create(
                    current_weight=current_weight,
                    duration_weeks=duration_weeks,
                    weight_change_kg=round(predicted_weight_change_kg, 2),
                    physical_activity_level=physical_activity_level
                )
            except Exception as e:
                print(f"Error saving weight prediction: {e}")
                # Don't fail the whole prediction if DB save fails
                pass

            context = {
                'prediction': round(predicted_weight_change_kg, 2),
                'current_weight': current_weight,
                'target_weight': target_weight,
                'duration_weeks': duration_weeks,
                'physical_activity_level': physical_activity_level,
                'age': age,
                'gender': gender,
                'weight_difference': round(weight_difference_kg, 2),
                'weekly_change_needed': round(weekly_change_needed, 2),
                'daily_calorie_adjustment': round(daily_calorie_adjustment, 0),
                'daily_calorie_adjustment_abs': abs(round(daily_calorie_adjustment, 0))
            }

            return render(request, 'weight_change_prediction.html', context)

        except Exception as e:
            messages.error(request, f'Error making prediction: {str(e)}')
            return render(request, 'weight_change_prediction.html')

    return render(request, 'weight_change_prediction.html')

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

            # Save the food recognition to database
            try:
                # Extract numeric values
                cal_val = float(calories.split()[0]) if calories != 'Not found' else 0
                prot_val = float(protein.split('g')[0]) if protein != 'Not found' else None
                carb_val = float(carbs.split('g')[0]) if carbs != 'Not found' else None
                fat_val = float(fat.split('g')[0]) if fat != 'Not found' else None

                FoodRecognition.objects.create(
                    recognized_food=food_label.title(),
                    calories=cal_val,
                    protein=prot_val,
                    carbs=carb_val,
                    fat=fat_val
                )
            except Exception as e:
                print(f"Error saving food recognition: {e}")

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

def saved_results(request):
    # Check if user is logged in
    if not request.user.is_authenticated or 'user_id' not in request.session:
        messages.warning(request, 'Please log in to view your saved results.')
        return redirect('login')

    # Get all saved results
    diet_plans = DietPlan.objects.all().order_by('-created_at')
    workout_plans = WorkoutPlan.objects.all().order_by('-created_at')
    weight_predictions = WeightPrediction.objects.all().order_by('-created_at')
    calorie_calculations = CalorieCalculation.objects.all().order_by('-created_at')
    food_recognitions = FoodRecognition.objects.all().order_by('-created_at')
    health_assessments = HealthAssessment.objects.all().order_by('-created_at')

    context = {
        'diet_plans': diet_plans,
        'workout_plans': workout_plans,
        'weight_predictions': weight_predictions,
        'calorie_calculations': calorie_calculations,
        'food_recognitions': food_recognitions,
        'health_assessments': health_assessments,
    }

    return render(request, 'saved_results.html', context)

def profile_view(request):
    # Check if user is logged in
    if not request.user.is_authenticated or 'user_id' not in request.session:
        messages.warning(request, 'Please log in to access your profile.')
        return redirect('login')

    try:
        user_profile = UserProfile.objects.get(id=request.session['user_id'])
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('login')

    if request.method == 'POST':
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            uploaded_file = request.FILES['profile_picture']
            if not uploaded_file:
                messages.error(request, 'Please select a file to upload.')
                return redirect('profile')
            # Validate file type
            if uploaded_file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                messages.error(request, 'Please upload a valid image file (JPEG, PNG, or GIF).')
                return redirect('profile')

            # Validate file size (max 5MB)
            if uploaded_file.size > 5 * 1024 * 1024:
                messages.error(request, 'Image file size must be less than 5MB.')
                return redirect('profile')

            # Delete old profile picture if exists
            if user_profile.profile_picture:
                user_profile.profile_picture.delete()

            # Save new profile picture
            user_profile.profile_picture = uploaded_file
            user_profile.save()
            messages.success(request, 'Profile picture updated successfully!')
            return redirect('profile')

        # Handle profile picture deletion
        elif 'delete_picture' in request.POST:
            if user_profile.profile_picture:
                user_profile.profile_picture.delete()
                user_profile.profile_picture = None
                user_profile.save()
                messages.success(request, 'Profile picture deleted successfully!')
            else:
                messages.warning(request, 'No profile picture to delete.')
            return redirect('profile')

        # Handle profile information update
        else:
            user_profile.name = request.POST.get('name', user_profile.name)
            user_profile.age = request.POST.get('age', user_profile.age)
            user_profile.weight = request.POST.get('weight', user_profile.weight)
            user_profile.goal = request.POST.get('goal', user_profile.goal)
            user_profile.save()

            # Sync session with updated profile
            request.session['user_name'] = user_profile.name
            request.session['user_email'] = user_profile.email
            request.session['user_goal'] = user_profile.goal

            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')

    user_profile_pic_url = user_profile.profile_picture.url if user_profile.profile_picture else ''
    context = {
        'user_profile': user_profile,
        'user_profile_pic_url': user_profile_pic_url,
    }
    return render(request, 'profile.html', context)

def logout_view(request):
    # Use Django's logout to properly clear authentication
    django_logout(request)
    # Also clear our custom session variables
    request.session.flush()
    # Force clear any remaining allauth/social auth session data
    keys_to_delete = [key for key in request.session.keys() if 'allauth' in key.lower() or 'social' in key.lower()]
    for key in keys_to_delete:
        del request.session[key]
    # Clear any remaining user-related session data
    if 'user_id' in request.session:
        del request.session['user_id']
    if 'user_name' in request.session:
        del request.session['user_name']
    if 'user_email' in request.session:
        del request.session['user_email']
    if 'user_goal' in request.session:
        del request.session['user_goal']
    messages.success(request, 'You have been logged out successfully.')
    return redirect('landing')

def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        goal = request.POST.get("goal", "maintain_weight")  # default agar user ne goal na diya

        # Validate email format
        if not email or '@' not in email or '.' not in email:
            messages.error(request, "The email provided is incorrect. Please enter a valid email address.")
            return render(request, "register.html")

        # Check if user already exists
        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "An account with this email is already generated. Please log in instead.")
            return redirect("login")

        # Validate password length
        if not password or len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, "register.html")

        # Save new user
        user_profile = UserProfile.objects.create(
            name=name if name else "User",
            email=email,
            password=make_password(password),
            goal=goal
        )

        # Session me store kar ke auto-login
        request.session["user_id"] = user_profile.id
        request.session["user_name"] = user_profile.name
        request.session["user_email"] = user_profile.email
        request.session["user_goal"] = user_profile.goal

        messages.success(request, "Account created successfully!")

        return redirect("landing")

    return render(request, "register.html")
