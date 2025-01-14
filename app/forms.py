from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = UserProfile
        fields = [
            'user_type', 
            'first_name', 
            'last_name', 
            'profile_picture', 
            'username', 
            'email', 
            'password', 
            'confirm_password', 
            'address_line1', 
            'city', 
            'state', 
            'pincode',
        ]
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match. Please enter them again.")
        
        return cleaned_data