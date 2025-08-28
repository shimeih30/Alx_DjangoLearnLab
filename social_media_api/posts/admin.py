from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for Post model
    """
    list_display = ['title', 'author', 'comments_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['title', 'content', 'author__username']
    readonly_fields = ['created_at', 'updated_at', 'comments_count']
    ordering = ['-created_at']
    
    def comments_count(self, obj):
        return obj.comments.count()
    comments_count.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for Comment model
    """
    list_display = ['get_post_title', 'author', 'get_content_preview', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'author']
    search_fields = ['content', 'author__username', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_post_title(self, obj):
        return obj.post.title
    get_post_title.short_description = 'Post'
    get_post_title.admin_order_field = 'post__title'
    
    def get_content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    get_content_preview.short_description = 'Content Preview'