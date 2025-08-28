from rest_framework import serializers
from .models import Post, Comment
from accounts.serializers import PublicUserProfileSerializer

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model
    """
    author = PublicUserProfileSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'content', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        Create and return a new comment instance
        """
        validated_data['author'] = self.context['request'].user
        return Comment.objects.create(**validated_data)

class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating comments (simplified)
    """
    class Meta:
        model = Comment
        fields = ['content']

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model with full details
    """
    author = PublicUserProfileSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'content', 'image',
            'comments', 'comments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        Create and return a new post instance
        """
        validated_data['author'] = self.context['request'].user
        return Post.objects.create(**validated_data)

class PostListSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model in list view (without comments)
    """
    author = PublicUserProfileSerializer(read_only=True)
    comments_count = serializers.ReadOnlyField()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'content', 'image',
            'comments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating posts
    """
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        
    def validate_title(self, value):
        """
        Validate that title is not empty or just whitespace
        """
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty")
        return value.strip()
    
    def validate_content(self, value):
        """
        Validate that content is not empty or just whitespace
        """
        if not value.strip():
            raise serializers.ValidationError("Content cannot be empty")
        return value.strip()