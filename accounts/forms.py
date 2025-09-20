
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class SignUpForm(UserCreationForm):
    # This correctly makes the email field required on the form
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        # Only include fields that are part of the User model itself
        fields = ('username', 'email')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # List the fields from your Profile model that you want to be editable
        fields = ['bio', 'location', 'profile_picture']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'hidden'}),
        }
    