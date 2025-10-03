from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    # This creates a one-to-one link with Django's built-in User model.
    # Each user will have exactly one profile.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    # Custom fields you want to add to the user
    bio = models.TextField(blank=True, null=True)
    #profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    
    # This creates a many-to-many relationship for the friend list.
    # A profile can be friends with many other profiles.
    friends = models.ManyToManyField("self", blank=True, symmetrical=False)

    def __str__(self):
        return f'{self.user.username} Profile'



