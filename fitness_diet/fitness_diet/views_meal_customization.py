from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, MealPlan, MealSwap, FoodDatabase

def customize_meals(request):
    """View for customizing meal plans"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Please log in to customize your meals.')
        return redirect('login')

    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        messages.error(request, 'User profile not found.')
        return redirect('login')

    if request.method == 'POST':
        # Process save changes action
        meal_ids = request.POST.getlist('meal_id')
        food_items = request.POST.getlist('food_item')
        calories_list = request.POST.getlist('calories')

        for meal_id, food_item, calories in zip(meal_ids, food_items, calories_list):
            try:
                meal = MealPlan.objects.get(id=meal_id, user=user)
                meal.food_item = food_item
                meal.calories = int(calories)
                meal.save()
            except MealPlan.DoesNotExist:
                continue

        messages.success(request, 'Changes saved successfully.')
        return redirect('gain_weight_plan')  # Redirect to gain weight plan with dashboard hash

    # Get current meal plan for the user
    current_meals = MealPlan.objects.filter(user=user)

    # If no meals exist, create default ones
    if not current_meals.exists():
        default_meals = [
            {'meal_type': 'breakfast', 'food_item': 'Oatmeal with Berries', 'calories': 350},
            {'meal_type': 'lunch', 'food_item': 'Grilled Chicken Salad', 'calories': 450},
            {'meal_type': 'dinner', 'food_item': 'Salmon with Roasted Vegetables', 'calories': 500},
        ]
        for meal_data in default_meals:
            MealPlan.objects.create(user=user, **meal_data)
        current_meals = MealPlan.objects.filter(user=user)

    # Get available food options from database
    available_foods = FoodDatabase.objects.all()[:20]  # Limit for performance

    context = {
        'current_meals': current_meals,
        'available_foods': available_foods,
        'user': user,
    }

    return render(request, 'customize_meals.html', context)

@csrf_exempt
def swap_meal(request):
    """AJAX view to handle meal swapping"""
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'error': 'Please log in first.'}, status=401)

        try:
            user = UserProfile.objects.get(id=user_id)
            meal_id = request.POST.get('meal_id')
            new_food = request.POST.get('new_food')
            new_calories = request.POST.get('new_calories')
            swap_reason = request.POST.get('swap_reason', 'preference')

            # Get the original meal
            original_meal = MealPlan.objects.get(id=meal_id, user=user)

            # Create meal swap record
            MealSwap.objects.create(
                user=user,
                original_meal=original_meal,
                swapped_food=new_food,
                swapped_calories=int(new_calories),
                swap_reason=swap_reason
            )

            # Update the meal plan
            original_meal.food_item = new_food
            original_meal.calories = int(new_calories)
            original_meal.save()

            return JsonResponse({
                'success': True,
                'message': f'Successfully swapped {original_meal.get_meal_type_display()} to {new_food}'
            })

        except MealPlan.DoesNotExist:
            return JsonResponse({'error': 'Meal not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)
