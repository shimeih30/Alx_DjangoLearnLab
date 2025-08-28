from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration
    """
    password = serializers.CharField(
        write_only=True, 
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'profile_picture', 'password', 'password_confirm'
        )
        extra_kwargs = {
            'email': {'required': True},
        }
    
    def validate(self, attrs):
        """
        Validate that passwords match
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        """
        Create and return a new user instance
        """
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login
    """
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        """
        Validate and authenticate the user
        """
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include username and password')

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile (read and update)
    """
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'profile_picture', 'followers_count', 'following_count',
            'date_joined', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'username', 'date_joined', 'created_at', 'updated_at')

class PublicUserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for public user profiles (limited information)
    """
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = (
            'id', 'username', 'first_name', 'last_name',
            'bio', 'profile_picture', 'followers_count', 'following_count',
            'date_joined'
        )
        
    ["from rest_framework.authtoken.models import Token", "Token.objects.create", "get_user_model().objects.create_user"]