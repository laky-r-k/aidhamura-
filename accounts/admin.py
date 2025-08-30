from django.contrib import admin

# Register your models here.
# accounts/admin.py
from .models import Profile # Import your Profile model

# This line tells Django to show the Profile model in the admin interface
admin.site.register(Profile)