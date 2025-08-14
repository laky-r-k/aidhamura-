from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        # Define the common CSS class for all fields
        common_classes = "w-full bg-gray-900/50 border border-white/10 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"

        # Add the CSS classes to the widgets of each field
        self.fields['username'].widget.attrs.update({'class': common_classes, 'placeholder': 'Create a username'})
        self.fields['email'].widget.attrs.update({'class': common_classes, 'placeholder': 'Enter your email'})
        self.fields['password'].widget.attrs.update({'class': common_classes, 'placeholder': 'Enter a secure password'})
        self.fields['password2'].widget.attrs.update({'class': common_classes, 'placeholder': 'Confirm your password'})

    class Meta:
        model = User
        fields = ('username', 'email')