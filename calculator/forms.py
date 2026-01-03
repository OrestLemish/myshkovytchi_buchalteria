from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, DailyRecord, Meal

class MealForm(forms.ModelForm):
    """Form for creating and editing meals"""
    class Meta:
        model = Meal
        fields = ['name', 'meal_type', 'time', 'calories', 'proteins', 'fats', 'carbs']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-style'}),
            'meal_type': forms.Select(attrs={'class': 'input-style'}),
            'time': forms.TimeInput(attrs={'class': 'input-style', 'type': 'time'}),
            'calories': forms.NumberInput(attrs={'class': 'input-style', 'min': '0'}),
            'proteins': forms.NumberInput(attrs={'class': 'input-style', 'min': '0', 'step': '0.1'}),
            'fats': forms.NumberInput(attrs={'class': 'input-style', 'min': '0', 'step': '0.1'}),
            'carbs': forms.NumberInput(attrs={'class': 'input-style', 'min': '0', 'step': '0.1'}),
        }

class DailyRecordForm(forms.ModelForm):
    """Form for creating daily records"""
    class Meta:
        model = DailyRecord
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'input-style', 'type': 'date'}),
        }

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = CustomUser
        fields = ['target_calories', 'target_proteins', 'target_fats', 'target_carbs']
        widgets = {
            'target_calories': forms.NumberInput(attrs={'class': 'input-style', 'min': '0'}),
            'target_proteins': forms.NumberInput(attrs={'class': 'input-style', 'min': '0', 'step': '0.1'}),
            'target_fats': forms.NumberInput(attrs={'class': 'input-style', 'min': '0', 'step': '0.1'}),
            'target_carbs': forms.NumberInput(attrs={'class': 'input-style', 'min': '0', 'step': '0.1'}),
        }

class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users with nutritional goals"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input-style'}))
    target_calories = forms.IntegerField(
        required=False, 
        initial=2000,
        widget=forms.NumberInput(attrs={'class': 'input-style', 'min': '0'})
    )
    target_proteins = forms.FloatField(
        required=False, 
        initial=150,
        widget=forms.NumberInput(attrs={'class': 'input-style', 'min': '0', 'step': '0.1'})
    )
    target_fats = forms.FloatField(
        required=False, 
        initial=70,
        widget=forms.NumberInput(attrs={'class': 'input-style', 'min': '0', 'step': '0.1'})
    )
    target_carbs = forms.FloatField(
        required=False, 
        initial=250,
        widget=forms.NumberInput(attrs={'class': 'input-style', 'min': '0', 'step': '0.1'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 
                 'target_calories', 'target_proteins', 'target_fats', 'target_carbs']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'input-style'})
        self.fields['password1'].widget.attrs.update({'class': 'input-style'})
        self.fields['password2'].widget.attrs.update({'class': 'input-style'})
