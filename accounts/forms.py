
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from allauth.account.forms import LoginForm
class SignUpForm(UserCreationForm):
    # This correctly makes the email field required on the form
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        # Only include fields that are part of the User model itself
        fields = ('username', 'email')


# accounts/forms.py


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        # Here you can add or remove fields, or add custom attributes
        self.fields['login'].widget.attrs.update({'class': 'custom-input-class'})
        self.fields['password'].widget.attrs.update({'class': 'custom-input-class'})

    def clean(self):
        # You can add custom validation logic here
        return super(CustomLoginForm, self).clean()
    


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        help_texts = {
            'username': None, # This hides the default help text to keep the form clean
        }

# This form will handle the fields from your custom Profile model
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        # The fields should match what's in your template: bio, location, profile_picture
        fields = ['bio', 'location', 'profile_picture']