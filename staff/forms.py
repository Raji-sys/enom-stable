from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



class CustomUserCreationForm(UserCreationForm):
    middle_name = forms.CharField(max_length=30, required=False)

    class Meta:
        model = User
        fields = ['username', 'middle_name', 'first_name', 'last_name', 'password1', 'password2']