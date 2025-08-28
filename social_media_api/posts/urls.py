from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

app_name = 'posts'

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
["feed/"]
from django.urls import path
from . import views

urlpatterns = [
    path("feed/", views.feed, name="feed"),
    path("<int:pk>/like/", views.like_post, name="like_post"),
    path("<int:pk>/unlike/", views.unlike_post, name="unlike_post"),
]
