from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Follow

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin for CustomUser model
    """
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'followers_count', 'following_count', 'is_active', 'date_joined'
    )
    
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'date_joined'
    )
    
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    ordering = ('username',)
    
    # Add custom fields to the user form
    fieldsets = UserAdmin.fieldsets + (
        ('Social Media Info', {
            'fields': ('bio', 'profile_picture')
        }),
    )
    
    # Add custom fields to the add user form
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Social Media Info', {
            'fields': ('bio', 'profile_picture')
        }),
    )

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Admin for Follow model
    """
    list_display = ('follower', 'followed', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'followed__username')
    raw_id_fields = ('follower', 'followed')