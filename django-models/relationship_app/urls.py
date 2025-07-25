from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),
]
from .views import list_books, 
LibraryDetailView

from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import list_books, LibraryDetailView, register

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', register, name='register'),
]
views.register
from django.urls import path
from .views import admin_view, librarian_view, member_view

urlpatterns = [
    # ... existing URLs ...
    path('admin/dashboard/', admin_view, name='admin_view'),
    path('librarian/dashboard/', librarian_view, name='librarian_view'),
    path('member/dashboard/', member_view, name='member_view'),
]
add_book/
edit_book/ 
delete_book