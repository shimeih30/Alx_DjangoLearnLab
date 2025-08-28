from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Post, Comment
from .serializers import (
    PostSerializer, PostListSerializer, PostCreateUpdateSerializer,
    CommentSerializer, CommentCreateSerializer
)
from .permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing posts
    """
    queryset = Post.objects.all().select_related('author').prefetch_related('comments__author')
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    filterset_fields = ['author']
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action
        """
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostCreateUpdateSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        """
        Set the author of the post to the current user
        """
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_comment(self, request, pk=None):
        """
        Add a comment to a specific post
        """
        post = self.get_object()
        serializer = CommentCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            comment = serializer.save(author=request.user, post=post)
            response_serializer = CommentSerializer(comment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Get all comments for a specific post
        """
        post = self.get_object()
        comments = post.comments.all().select_related('author')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_posts(self, request):
        """
        Get posts created by the current user
        """
        posts = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(posts)
        
        if page is not None:
            serializer = PostListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments
    """
    queryset = Comment.objects.all().select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['post', 'author']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on action
        """
        if self.action in ['create', 'update', 'partial_update']:
            return CommentCreateSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        """
        Set the author of the comment to the current user
        """
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_comments(self, request):
        """
        Get comments created by the current user
        """
        comments = self.queryset.filter(author=request.user)
        page = self.paginate_queryset(comments)
        
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    "Post.objects.filter(author__in=following_users).order_by", "following.all()"
    ["generics.get_object_or_404(Post, pk=pk)", "Like.objects.get_or_create(user=request.user, post=post)", "Notification.objects.create"]
    from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Post, Like
from .serializers import PostSerializer
from notifications.models import Notification

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # prevent duplicate likes
    if Like.objects.filter(user=request.user, post=post).exists():
        return Response({"detail": "You already liked this post."}, status=400)

    Like.objects.create(user=request.user, post=post)

    # create notification for post author
    if post.author != request.user:
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )

    return Response({"detail": "Post liked."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like = Like.objects.filter(user=request.user, post=post).first()

    if not like:
        return Response({"detail": "You haven’t liked this post."}, status=400)

    like.delete()
    return Response({"detail": "Post unliked."})
