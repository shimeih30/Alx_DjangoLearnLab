from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    PublicUserProfileSerializer
)

class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'User created successfully',
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    API endpoint for user login
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Get or create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Login successful',
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_logout(request):
    """
    API endpoint for user logout
    """
    try:
        # Delete the user's token to log them out
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({
            'error': 'No active session found'
        }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating user profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class PublicUserProfileView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving public user profiles
    """
    queryset = CustomUser.objects.all()
    serializer_class = PublicUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'

@api_view(['GET'])
def user_list(request):
    """
    API endpoint to list all users (for testing purposes)
    """
    users = CustomUser.objects.all()
    serializer = PublicUserProfileSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def follow_user(request, username):
    """
    API endpoint to follow a user
    """
    try:
        user_to_follow = CustomUser.objects.get(username=username)
        if user_to_follow == request.user:
            return Response({
                'error': 'You cannot follow yourself'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        request.user.following.add(user_to_follow)
        return Response({
            'message': f'You are now following {username}'
        }, status=status.HTTP_200_OK)
        
    except CustomUser.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def unfollow_user(request, username):
    """
    API endpoint to unfollow a user
    """
    try:
        user_to_unfollow = CustomUser.objects.get(username=username)
        request.user.following.remove(user_to_unfollow)
        return Response({
            'message': f'You have unfollowed {username}'
        }, status=status.HTTP_200_OK)
        
    except CustomUser.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)