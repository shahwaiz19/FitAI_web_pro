from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    goal = models.CharField(max_length=50, choices=[
        ('lose_weight', 'Lose Weight'),
        ('gain_weight', 'Gain Weight'),
        ('maintain_weight', 'Maintain Weight'),
    ])
    age = models.IntegerField()
    sex = models.CharField(max_length=10, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ])
    height = models.FloatField()  # in cm
    weight = models.FloatField()  # in kg
    weekly_goal = models.CharField(max_length=50, choices=[
        ('lose_0.5', 'Lose 0.5kg per week'),
        ('lose_1', 'Lose 1kg per week'),
        ('maintain', 'Maintain weight'),
        ('gain_0.5', 'Gain 0.5kg per week'),
        ('gain_1', 'Gain 1kg per week'),
    ])
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Store hashed password
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['name', 'goal', 'age', 'sex', 'height', 'weight', 'weekly_goal']

    def __str__(self):
        return self.name

class MealPlan(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=20, choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ])
    food_item = models.CharField(max_length=200)
    calories = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'meal_type']

    def __str__(self):
        return f"{self.user.name} - {self.meal_type}: {self.food_item}"

class MealSwap(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    original_meal = models.ForeignKey(MealPlan, on_delete=models.CASCADE, related_name='original_meals')
    swapped_food = models.CharField(max_length=200)
    swapped_calories = models.IntegerField()
    swap_reason = models.CharField(max_length=100, choices=[
        ('preference', 'Personal Preference'),
        ('dietary', 'Dietary Restriction'),
        ('variety', 'Want Variety'),
        ('availability', 'Food Availability'),
    ], default='preference')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} swapped {self.original_meal.food_item} for {self.swapped_food}"

class FoodDatabase(models.Model):
    name = models.CharField(max_length=200, unique=True)
    calories = models.IntegerField()
    protein = models.FloatField(null=True, blank=True)  # in grams
    carbs = models.FloatField(null=True, blank=True)    # in grams
    fat = models.FloatField(null=True, blank=True)      # in grams
    category = models.CharField(max_length=50, choices=[
        ('vegetarian', 'Vegetarian'),
        ('vegan', 'Vegan'),
        ('high_protein', 'High Protein'),
        ('low_carb', 'Low Carb'),
        ('gluten_free', 'Gluten Free'),
        ('dairy_free', 'Dairy Free'),
    ], blank=True)
    is_healthy = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"
