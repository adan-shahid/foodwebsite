from django import forms
from .models import User

class userRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','password']