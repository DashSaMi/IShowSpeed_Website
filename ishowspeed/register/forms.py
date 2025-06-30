from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from register.models import CustomUser  # Make sure to import your custom user

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    verification_code = forms.CharField(required=True)
   
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1',)

 
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 7:
            raise ValidationError("Username must be at least 7 characters long.")
        return username

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 9:
            raise ValidationError("Password must be at least 9 characters long.")
        return password

    def clean_verification_code(self):
        code = self.cleaned_data.get('verification_code')
        session_code = self.request.session.get('verification_code') if self.request else None
        if not code or code != session_code:
            raise ValidationError("Invalid verification code.")
        return code
    