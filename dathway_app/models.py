from django.db import models
from django.contrib.auth.models import User
from datetime import datetime




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_dp_image', blank=True)
    cover_picture = models.ImageField(upload_to='profile_cover_image', blank=True)
    bio = models.TextField(blank=True)
    joined = models.DateTimeField( default=datetime.now)
    followers = models.ManyToManyField('Profile', related_name='profile_followers', blank=True)
    following = models.ManyToManyField('Profile', related_name='profile_following', blank=True)
    interests = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return f"{self.user.username}"
    

class ChatMessage(models.Model):
    message = models.TextField()
    participants = models.ManyToManyField(Profile, related_name="conversations")
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notification')
    timestamp = models.DateTimeField(auto_now_add=True)

