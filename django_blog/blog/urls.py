from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import add_comment, CommentUpdateView, CommentDeleteView


urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="blog/logout.html"), name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
]

from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]
["post/<int:pk>/delete/", "post/<int:pk>/update/", "post/new/"]

urlpatterns += [
    path("posts/<int:pk>/comments/new/", add_comment, name="add-comment"),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="edit-comment"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="delete-comment"),
]
