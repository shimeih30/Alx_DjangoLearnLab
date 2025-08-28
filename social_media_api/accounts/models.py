from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    with additional fields for social media functionality
    """
    bio = models.TextField(
        max_length=500, 
        blank=True, 
        help_text="Tell us about yourself"
    )
    
    profile_picture = models.ImageField(
        upload_to='profile_pics/', 
        blank=True, 
        null=True,
        help_text="Upload your profile picture"
    )
    
    followers = models.ManyToManyField(
        'self', 
        through='Follow',
        related_name='following',
        symmetrical=False,
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.username
    
    @property
    def followers_count(self):
        """Return the count of followers"""
        return self.followers.count()
    
    @property
    def following_count(self):
        """Return the count of users this user is following"""
        return self.following.count()

class Follow(models.Model):
    """
    Through model for the followers relationship
    to add timestamps and additional functionality
    """
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following_set'
    )
    
    followed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers_set'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'followed')
        
    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"