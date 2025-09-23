from django import forms
from .models import UserProfile

class OnboardingWelcomeForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your name",
            "class": "w-full px-3 py-2 border border-gray-300 rounded-lg text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#11d452]"
        })
    )

class OnboardingGoalForm(forms.Form):
    goal = forms.ChoiceField(choices=[
        ('lose_weight', 'Lose Weight'),
        ('gain_weight', 'Gain Weight'),
        ('maintain_weight', 'Maintain Weight'),
    ], widget=forms.RadioSelect, required=True)

class OnboardingInfoForm(forms.Form):
    age = forms.IntegerField(min_value=1, max_value=120, required=True, widget=forms.NumberInput(attrs={'placeholder': 'e.g. 25', 'class': 'pl-10'}))
    sex = forms.ChoiceField(choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], widget=forms.Select(attrs={'class': 'pl-10'}), required=True)
    height = forms.FloatField(min_value=50, max_value=250, required=True, widget=forms.NumberInput(attrs={'placeholder': 'e.g. 175', 'class': 'pl-10'}))
    weight = forms.FloatField(min_value=20, max_value=300, required=True, widget=forms.NumberInput(attrs={'placeholder': 'e.g. 70', 'class': 'pl-10'}))
    weekly_goal = forms.ChoiceField(choices=[
        ('lose_0.5', 'Lose 0.5kg per week'),
        ('lose_1', 'Lose 1kg per week'),
        ('maintain', 'Maintain weight'),
        ('gain_0.5', 'Gain 0.5kg per week'),
        ('gain_1', 'Gain 1kg per week'),
    ], widget=forms.Select(attrs={'class': 'pl-10'}), required=True)

class OnboardingAccountForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(min_length=6, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
