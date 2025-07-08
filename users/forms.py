from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'street_address', 'city', 'postal_code')

class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    class Meta(UserChangeForm.Meta):
        model = User
        fields = '__all__'

class UserProfileForm(forms.ModelForm):
    """
    A form for users to update their own profile information.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'street_address', 'city', 'postal_code')